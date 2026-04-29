/* eslint-disable react/prop-types */
import React from "react";
import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
  Typography,
  Box,
  Card,
  CardContent,
  Stack,
  Icon,
} from "@mui/material";

// The Dialog component that displays the scope data.
const DialogScope = ({
  open,
  onClose,
  data,
  onSearchSelected,
  bookInitData,
}) => {
  if (!data) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth dir="rtl">
      <DialogTitle>
        <Stack
          direction="row-reverse"
          justifyContent="space-between"
          alignItems="center"
        >
          <IconButton onClick={onClose} aria-label="close">
            <Icon sx={{ color: "black" }}>close</Icon>
          </IconButton>
          <Typography color="black" variant="h6">
            البحث العميق
          </Typography>
        </Stack>
      </DialogTitle>
      <DialogContent dividers>
        <Stack spacing={2}>
          {data.scopes_small_to_big.map((scope, index) => {
            const range = scope.endPage - scope.startPage;
            const showSearchButton = range < bookInitData.search_range;

            return (
              <Card key={scope.id} variant="outlined" sx={{ borderRadius: 2 }}>
                <CardContent
                  sx={{
                    display: "flex",
                    flexDirection: { xs: "column", sm: "row-reverse" },
                    justifyContent: "space-between",
                    alignItems: "center",
                  }}
                >
                  <Box sx={{ flexGrow: 1, mb: { xs: 1, sm: 0 } }}>
                    <Typography
                      color="primary.main"
                      variant="h6"
                      component="h3"
                      sx={{ fontWeight: "bold" }}
                    >
                      {scope.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      الصفحات: {scope.startPage} - {scope.endPage}
                    </Typography>
                  </Box>
                </CardContent>
                {showSearchButton && (
                  <Button
                    variant="contained"
                    onClick={() => {
                      onSearchSelected(scope);
                      onClose();
                    }}
                    sx={{
                      px: 3,
                      m: 3,
                      py: 1,
                      bgcolor: "secondary.main",
                      borderRadius: 1,
                      "&:hover": { bgcolor: "secondary.dark" },
                    }}
                  >
                    إبحث هنا
                  </Button>
                )}
              </Card>
            );
          })}
        </Stack>
      </DialogContent>
    </Dialog>
  );
};

export default DialogScope;
