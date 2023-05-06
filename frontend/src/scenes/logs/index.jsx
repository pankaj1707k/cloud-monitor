import { Box, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useEffect, useState } from "react";
import Header from "../../components/Header";
import { tokens } from "../../theme";

const Logs = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  var [logs, setLogs] = useState([]);

  const API_URL = "http://localhost:8000/api/log/get";

  useEffect(() => {
    async function getLogs() {
      const result = await fetch(API_URL);
      if (!ignore) {
        setLogs(result);
      }
    }

    let ignore = false;
    getLogs();
    return () => {
      ignore = true;
    };
  }, [logs]);

  const columns = [
    { field: "machine_id", headerName: "Machine ID", flex: 0.5 },
    { field: "log_filepath", headerName: "Log file" },
    {
      field: "timestamp",
      headerName: "Timestamp",
      type: "number",
      headerAlign: "left",
    },
    {
      field: "type",
      headerName: "Type",
      flex: 1,
      align: "left",
    },
    {
      field: "content",
      headerName: "Content",
      flex: 1,
    },
  ];

  return (
    <Box m="20px">
      <Header title="Logs" />
      <Box
        m="40px 0 0 0"
        height="75vh"
        sx={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
          "& .MuiDataGrid-cell": {
            borderBottom: "none",
          },
          "& .name-column--cell": {
            color: colors.greenAccent[300],
          },
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: colors.blueAccent[700],
            borderBottom: "none",
          },
          "& .MuiDataGrid-virtualScroller": {
            backgroundColor: colors.primary[400],
          },
          "& .MuiDataGrid-footerContainer": {
            borderTop: "none",
            backgroundColor: colors.blueAccent[700],
          },
          "& .MuiCheckbox-root": {
            color: `${colors.greenAccent[200]} !important`,
          },
        }}
      >
        <DataGrid rows={logs} columns={columns} />
      </Box>
    </Box>
  );
};

export default Logs;
