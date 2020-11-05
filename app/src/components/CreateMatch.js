import React, { useEffect, useState, useRef } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";
import { joinMatch } from "./../actions/match";
import { Slider, Rail, Handles, Tracks, Ticks } from "react-compound-slider";
import "./css/CreateMatch.css";
import {
  sliderStyle,
  railStyle,
  Handle,
  Track,
  Tick,
} from "./CreateMatchSliderProps";

function CreateMatch() {
  const dispatch = useDispatch();
  const history = useHistory();
  const isLogged = useSelector((state) => state.user.logged_in);
  const userID = useSelector((state) => state.user.id);
  const [isCreateMatchSuccess, setIsCreateMatchSuccess] = useState(false);
  const [minMaxPlayers, setMinMaxPlayers] = useState({
    minPlayers: 5,
    maxPlayers: 10,
  });
  const [matchProps, setMatchProps] = useState({
    userID: userID,
    minPlayers: minMaxPlayers.minPlayers,
    maxPlayers: minMaxPlayers.maxPlayers,
  });

  const updateMinMaxPlayers = (values) => {
    setMinMaxPlayers({ minPlayers: values[0], maxPlayers: values[1] });
  };

  const loaded = useRef(false);
  useEffect(() => {
    if (loaded.current) {
      createMatch();
    } else {
      loaded.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [matchProps]);

  const createMatch = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(
      url +
        `/game/new?minp=${minMaxPlayers.minPlayers}&maxp=${minMaxPlayers.maxPlayers}&uhid=${userID}`,
      {
        method: "POST",
      }
    )
      .then(async (response) => {
        const responseData = await response.json();
        if (response.status !== 200) {
          alert("Could not Create Match. Unknown Error.");
        } else {
          setIsCreateMatchSuccess(true);
          dispatch(joinMatch(responseData));
          history.push(`/match/${responseData.Match_id}`);
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  const getMatchProps = (e) => {
    e.preventDefault();
    if (minMaxPlayers.minPlayers > minMaxPlayers.maxPlayers) {
      alert("Min players can't be larger than max players!");
    } else {
      setMatchProps({
        userID: userID,
        minPlayers: minMaxPlayers.minPlayers,
        maxPlayers: minMaxPlayers.maxPlayers,
      });
    }
  };

  const createMatchFormJSX = (
    <div>
      {isLogged && !isCreateMatchSuccess ? (
        <div>
          <h1 className="title">Create Match</h1>
          <form onSubmit={getMatchProps} className="create-game-form">
            <label>
              Min Players
              <h1>{minMaxPlayers.minPlayers}</h1>
            </label>
            <label>
              Max Players
              <h1>{minMaxPlayers.maxPlayers}</h1>
            </label>
            <button className="create-button" type="submit">
              Create Match
            </button>
          </form>
          <Slider
            rootStyle={sliderStyle}
            domain={[5, 10]}
            step={1}
            mode={1}
            values={[5, 10]}
            onUpdate={updateMinMaxPlayers}
          >
            <Rail>
              {({ getRailProps }) => (
                <div style={railStyle} {...getRailProps()} />
              )}
            </Rail>
            <Handles>
              {({ handles, getHandleProps }) => (
                <div className="slider-handles">
                  {handles.map((handle) => (
                    <Handle
                      key={handle.id}
                      handle={handle}
                      getHandleProps={getHandleProps}
                    />
                  ))}
                </div>
              )}
            </Handles>
            <Tracks left={false} right={false}>
              {({ tracks, getTrackProps }) => (
                <div className="slider-tracks">
                  {tracks.map(({ id, source, target }) => (
                    <Track
                      key={id}
                      source={source}
                      target={target}
                      getTrackProps={getTrackProps}
                    />
                  ))}
                </div>
              )}
            </Tracks>
            <Ticks count={5}>
              {({ ticks }) => (
                <div className="slider-ticks">
                  {ticks.map((tick) => (
                    <Tick key={tick.id} tick={tick} count={ticks.length} />
                  ))}
                </div>
              )}
            </Ticks>
          </Slider>
        </div>
      ) : (
        ""
      )}
    </div>
  );

  return (
    <div>
      {createMatchFormJSX}
      {!isLogged && <h1>Please Log In to create match</h1>}
      {isCreateMatchSuccess && <h1>Success!</h1>}
    </div>
  );
}

export default CreateMatch;
