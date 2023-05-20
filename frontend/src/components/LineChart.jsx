import { Box, Typography, useTheme } from "@mui/material";
import { ResponsiveLine } from "@nivo/line";
import { useEffect, useState } from "react";
import { io } from "socket.io-client";
import { tokens } from "../theme";
import { HOST } from "../globals";
import {partial} from "filesize";
const size = partial({base: 2, standard: "jedec"});

const LineChart = ({ machine_id, title, is_bytes = false, path = "", isDashboard = false, yMin = "auto", yMax = "auto"}) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const URL = `${HOST}`;
  var [data, setData] = useState([]);
  var [_title, setTitle] = useState(title);

  useEffect(() => {
    const socket = io(URL);

    socket.on("receive_logs", (data) => {
      if (data.machine_id != machine_id) return;

      var logs = data.logs;      
      let prev = logs[Object.keys(logs)[0]].data.timestamp;

      // For use, when `is_bytes = true`
      var max_bytes = 0;

      var d = [{
        id: path,
        data: Object.keys(logs).map(timestamp => {
          let d = {
            x: timestamp - prev,
            y: logs[timestamp].data
          };

          if (path === null || path === "") return d;
    
          let sub = path.split(".");
    
          for (let s of sub) {
            d.y = d.y[s];
          }

          d.y = parseFloat(d.y);
          max_bytes = Math.max(d.y, max_bytes);
          return d;
        }),
      }];

      if (is_bytes) {
        let div = Math.pow(1024, Math.floor(Math.log2(max_bytes) / 10));
        let N = d[0].data.length;
        
        let speed = size(d[0].data[N - 1].y);
        let new_title = `${_title} - ${speed}/s`;
        setTitle(new_title);

        for (let i = 0; i < N; i++) {
          d[0].data[i].y /= div;
        }
      }

      setData(d);
    });

    return () => socket.disconnect();
  }, []);

  return (<>
  <Box
      gridColumn="span 4"
      gridRow="span 2"
      backgroundColor={colors.primary[400]}
    >
      <Box
        mt="20px"
        p="0 10px"
        display="flex "
        justifyContent="space-between"
        alignItems="center"
      >
        <Box>
          <Typography
            variant="h3"
            fontWeight="800"
            color={colors.grey[100]}
          >
            {_title}
          </Typography>
        </Box>
      </Box>
      <Box height="240px" m="-20px 0 0 20px">
        <ResponsiveLine
          animate={false}
          data={data}
          theme={{
            axis: {
              domain: {
                line: {
                  stroke: colors.grey[100],
                },
              },
              legend: {
                text: {
                  fill: colors.grey[100],
                },
              },
              ticks: {
                line: {
                  stroke: colors.grey[100],
                  strokeWidth: 1,
                },
                text: {
                  fill: colors.grey[100],
                },
              },
            },
            legends: {
              text: {
                fill: colors.grey[100],
              },
            },
            tooltip: {
              container: {
                color: colors.primary[500],
              },
            },
          }}
          colors={isDashboard ? { datum: "color" } : { scheme: "nivo" }} // added
          margin={{ top: 50, right: 110, bottom: 50, left: 80 }}
          xScale={{ type: "point" }}
          yScale={{
            type: "linear",
            min: yMin,
            max: yMax,
            stacked: true,
            reverse: false,
          }}
          yFormat=" >-.2f"
          curve="catmullRom"
          axisTop={null}
          axisRight={null}
          axisBottom={{
            orient: "bottom",
            tickSize: 0,
            tickPadding: 5,
            tickRotation: 0,
            legend: isDashboard ? undefined : "", // added
            legendOffset: 36,
            legendPosition: "middle",
          }}
          axisLeft={{
            orient: "left",
            tickValues: 5, // added
            tickSize: 3,
            tickPadding: 5,
            tickRotation: 0,
            legend: isDashboard ? undefined : "", // added
            legendOffset: -40,
            legendPosition: "middle",
          }}
          enableGridX={false}
          enableGridY={false}
          pointSize={4}
          pointColor={{ theme: "background" }}
          pointBorderWidth={1}
          pointBorderColor={{ from: "serieColor" }}
          pointLabelYOffset={-12}
          useMesh={true}
          legends={[
            {
              anchor: "top-right",
              direction: "column",
              justify: false,
              translateX: 40,
              translateY: -40,
              itemsSpacing: 0,
              itemDirection: "left-to-right",
              itemWidth: 80,
              itemHeight: 20,
              itemOpacity: 0.75,
              symbolSize: 12,
              symbolShape: "circle",
              symbolBorderColor: "rgba(0, 0, 0, .5)",
              effects: [
                {
                  on: "hover",
                  style: {
                    itemBackground: "rgba(0, 0, 0, .03)",
                    itemOpacity: 1,
                  },
                },
              ],
            },
          ]}
        />
      </Box>
    </Box>
  </>);
};

export default LineChart;
