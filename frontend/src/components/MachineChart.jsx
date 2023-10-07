import { Box, Typography } from "@mui/material";
import LineChart from "./LineChart";

import { useEffect, useState } from "react";
import { io } from "socket.io-client";

import { HOST } from "../globals";

const MachineChart = ({ hostname = "", machine_id}) => {
  const URL = `${HOST}`;
  var [data, setData] = useState({});

  useEffect(() => {
    const socket = io(URL);

    socket.on("receive_logs", (data) => {
      if (data.machine_id === machine_id)
        setData(data);

      console.log(data);
    });

    return () => socket.disconnect();
  }, []);

  return (
    <Box mt="10px" mb="30px">
      <Box mb="8px">
        <Typography variant="h2">
          {hostname}
        </Typography>
      </Box>

      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="120px"
        gap="20px"
      >
        <LineChart data={data} title="CPU" path="cpu" yMin={0} yMax={100}></LineChart>
        <LineChart data={data} title="Memory" path="memory.primary" yMin={0} yMax={100}></LineChart>
        <LineChart data={data} title="Disk (read)" is_bytes={true} path="disk.read_bytes"></LineChart>
        <LineChart data={data} title="Disk (write)" is_bytes={true} path="disk.write_bytes"></LineChart>
        <LineChart data={data} title="Network (sent)" is_bytes={true} path="network.bytes_sent"></LineChart>
        <LineChart data={data} title="Network (recv)" is_bytes={true} path="network.bytes_recv"></LineChart>
      </Box>
    </Box>
  );
};

export default MachineChart;
