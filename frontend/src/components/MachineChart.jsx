import { Box, Typography } from "@mui/material";
import LineChart from "./LineChart";

const MachineChart = ({ hostname = "", machine_id}) => {
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
        <LineChart machine_id={machine_id} title="CPU" path="cpu" yMin={0} yMax={100}></LineChart>
        <LineChart machine_id={machine_id} title="Memory" path="memory.primary" yMin={0} yMax={100}></LineChart>
        <LineChart machine_id={machine_id} title="Disk (read)" unit="B/s" path="disk.read_bytes"></LineChart>
        <LineChart machine_id={machine_id} title="Disk (write)" unit="B/s" path="disk.write_bytes"></LineChart>
        <LineChart machine_id={machine_id} title="Network (sent)" unit="B/s" path="network.bytes_sent"></LineChart>
        <LineChart machine_id={machine_id} title="Network (recv)" unit="B/s" path="network.bytes_recv"></LineChart>  
      </Box>
    </Box>
  );
};

export default MachineChart;
