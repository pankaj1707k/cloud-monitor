import { Box, useTheme } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { useEffect, useState } from "react";
import Header from "../../components/Header";
import { tokens } from "../../theme";

const Events = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  var [events, setEvents] = useState([]);
  const API_URL = "http://10.10.10.185:3000/api/event/get?size=999&sort_order=DESC";

  useEffect(() => {
    async function getEvents() {
      const result = (await (await fetch(API_URL)).json()).data;

      if (!ignore) {
        setEvents(result);
      }
    }

    let ignore = false;
    getEvents();
    return () => {
      ignore = true;
    };
  }, []);

  const columns = [
    { field: "machine_id", headerName: "Machine ID", flex: 0.25 },
    { field: "log_filepath", headerName: "Log file", flex: 0.25 },
    {
      field: "timestamp",
      headerName: "Timestamp",
      type: "number",
      align: "left",
      flex: 0.125,
    },
    {
      field: "type",
      headerName: "Type",
      flex: 0.2,
      align: "left",
    },
    {
      field: "props",
      headerName: "Properties",
      flex: 1,
    },
  ];

  return (
    <Box m="20px">
      <Header title="Events" />
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
          "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
            color: `${colors.grey[100]} !important`,
          },
        }}
      >
        <DataGrid
          rows={events}
          columns={columns}
          components={{ Toolbar: GridToolbar }}
        />
      </Box>
    </Box>
  );
};

export default Events;
