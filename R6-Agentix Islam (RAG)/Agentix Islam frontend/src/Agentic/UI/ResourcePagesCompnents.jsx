/* eslint-disable react/prop-types */
import React from "react";
import { Box, Typography, Link, Paper, Grid, Icon } from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

// Create a custom MUI theme for a polished look and feel
const theme = createTheme({
  palette: {
    primary: {
      main: "#4caf50",
    },
    secondary: {
      main: "#f50057",
    },
  },
  typography: {
    fontFamily: "Inter, sans-serif",
    h4: {
      fontWeight: 600,
      color: "#333",
    },
    body1: {
      color: "#555",
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: "0 8px 30px rgba(0, 0, 0, 0.1)",
        },
      },
    },
    MuiLink: {
      styleOverrides: {
        root: {
          textDecoration: "none",
          color: "inherit",
          display: "block",
        },
      },
    },
    MuiAccordion: {
      styleOverrides: {
        root: {
          borderRadius: "16px !important",
          boxShadow: "0 8px 30px rgba(0, 0, 0, 0.1)",
          "&:before": {
            display: "none",
          },
        },
      },
    },
  },
});

// Main App component to display the resources
const ResourcePagesComponents = ({ searchData, bookInitData, onOpenPdf }) => {
  const book = searchData.ai_answer.resources;

  if (!book) {
    return (
      <Box
        sx={{ width: "100%", py: 4, px: { xs: 2, md: 3 }, direction: "rtl" }}
      >
        <Typography variant="body1" color="text.secondary" align="center">
          لا توجد بيانات للمصادر.
        </Typography>
      </Box>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <Box
        sx={{ width: "100%", py: 4, px: { xs: 2, md: 3 }, direction: "rtl" }}
      >
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Accordion defaultExpanded>
              <AccordionSummary
                expandIcon={<Icon sx={{ color: "black" }}>expand_more</Icon>}
                aria-controls={`panel-${book.book_id}-content`}
                id={`panel-${book.book_id}-header`}
              >
                <Box>
                  <Typography
                    color="primary.main"
                    variant="h6"
                    sx={{ fontWeight: "bold" }}
                  >
                    مصادر
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: "bold" }}>
                    {book.book_name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    إضغط على الصفحة لتزورها في الكتاب
                  </Typography>
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                <Grid container spacing={2}>
                  {book.length > 0 ? (
                    book.map((resource) => (
                      <Grid item xs={6} sm={4} key={resource.page_number}>
                        <Box
                          onClick={() => onOpenPdf(bookInitData.books_url[resource.book_part_number], resource.page_number + bookInitData.toc_offset)}
                          sx={{ 
                            width: "100%", 
                            display: 'block', 
                            textDecoration: 'none',
                            color: 'inherit',
                            cursor: 'pointer'
                          }}
                        >
                          <Paper
                            sx={{
                              p: 2,
                              display: "flex",
                              justifyContent: "center",
                              alignItems: "center",
                              transition: "transform 0.2s ease-in-out",
                              "&:hover": {
                                transform: "scale(1.05)",
                                cursor: "pointer",
                              },
                            }}
                          >
                            <Box>
                              <Typography color="black" variant="subtitle2">
                                صفحة {resource.page_number}
                              </Typography>
                              {resource.book_part_number !== 0 && (
                                <Typography color="black" variant="caption">
                                  الجزء {resource.book_part_number}
                                </Typography>
                              )}
                            </Box>
                          </Paper>
                        </Box>
                      </Grid>
                    ))
                  ) : (
                    <Grid item xs={12}>
                      <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{ mt: 1 }}
                      >
                        لا توجد مصادر متاحة.
                      </Typography>
                    </Grid>
                  )}
                </Grid>
              </AccordionDetails>
            </Accordion>
          </Grid>
        </Grid>
      </Box>
    </ThemeProvider>
  );
};

export default ResourcePagesComponents;
