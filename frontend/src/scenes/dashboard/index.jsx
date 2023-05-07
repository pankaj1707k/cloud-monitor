import { Box } from "@mui/material";
import Header from "../../components/Header";
import MachineChart from "../../components/MachineChart";

const Dashboard = () => {
  return (
    <Box m="20px">
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="Dashboard" />
      </Box>

      <MachineChart hostname="ubuntu-plain-vm" machine_id="fe14c4bc6c112596fdfa1bbb64572fa7"></MachineChart>
      <MachineChart hostname="ubuntu-malicious-vm" machine_id="4b2562e9fa6c4834bce25a92ec467804"></MachineChart>
    </Box>
  );
};

export default Dashboard;
