/* eslint-disable react/prop-types */
import React, { useState } from "react";
import {
  Box,
  Typography,
  Button,
  Paper,
  Stack,
  Icon,
  IconButton,
  Toolbar,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
  CircularProgress,
} from "@mui/material";
import ResourcePagesComponents from "./ResourcePagesCompnents";
import DialogScope from "./DialogScope";
import { apiUrl } from "../../api";

// A reusable component for displaying a search path item
const PathItem = ({ item, isLast }) => (
  <Paper
    variant={isLast ? "elevation" : "outlined"}
    elevation={isLast ? 3 : 0}
    sx={{
      p: 1.5,
      bgcolor: isLast ? "primary.main" : "background.paper",
      color: isLast ? "primary.contrastText" : "text.primary",
      textAlign: "right",
    }}
  >
    <Typography fontWeight="bold">{item.title}</Typography>
    <Typography variant="caption" display="block">
      الصفحات: {item.startPage} - {item.endPage}
    </Typography>
  </Paper>
);

const AgentixSearchHelper = ({
  searchData,
  bookInitData,
  onSearchSelected,
  closeDrawer,
  onOpenPdf,
}) => {
  const [scopeData, setScopeData] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [apiResponse, setApiResponse] = useState({});
  const [loading, setLoading] = useState({});

  // Return early if there is no data to display
  if (!searchData || !searchData.result) {
    return (
      <Box sx={{ p: 2, textAlign: "center" }}>
        <Typography>لا توجد نتائج بحث لعرضها.</Typography>
      </Box>
    );
  }

  // Safely destructure search results and relevant questions
  const { tree_search = [], similar_search = [] } = searchData.result;
  const relevant_questions = searchData.ai_answer?.relevant_questions || [];

  const handleSearchClick = (item) => {
    // Construct the query text to send back to the chat
    // Use item.startPage if available, otherwise use item.page_number
    const page =
      item.startPage !== undefined ? item.startPage : item.page_number;

    // Use a template literal (backticks) and \n for new lines to create a clearer message
    let query = `من الصفحة ${page}
من الجزء ${item.book_part_number}

إبحث بالتفصيل عن:
"${searchData.query}"
`;

    // A simpler version, using \n to separate the main components
    /*
    let query = `إبحث بالتفصيل عن  ""${searchData.query}"\nمن الصفحة ${page}\nمن الجزء ${item.book_part_number}`;
    */

    console.log(searchData);
    onSearchSelected(query);
  };

  const findPageScopes = async (bookId, pageNumber, book_part_number) => {
    try {
      const response = await fetch(
        // Corrected URL to include 'http://'
        `${apiUrl}/book/scope/${bookId}/${book_part_number}/${pageNumber}`,
        {
          // Correctly formatted headers
          headers: {
            Accept: "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const scopeData = await response.json();
      setScopeData(scopeData);
      setIsDialogOpen(true);
      console.log("Detailed search result:", scopeData);
      return scopeData;
    } catch (e) {
      console.error("Failed to perform detailed search:", e);
    }
  };

  // Function to simulate an API call
  const handleApiCall = async (topic, topicId) => {
    // Set loading state for the clicked button
    setLoading((prev) => ({ ...prev, [topicId]: true }));
    await findPageScopes(
      topic.book_id,
      topic.page_number,
      topic.book_part_number
    );
    const response = ""; // Hardcoded mock response
    setApiResponse((prev) => ({ ...prev, [topicId]: response }));
    setLoading((prev) => ({ ...prev, [topicId]: false }));
  };

  const handleQuestionClick = (question) => {
    // Calls the function with the selected question text
    onSearchSelected(question);
  };

  return (
    <Box sx={{ bgcolor: "#f8f8f8", height: "100%", direction: "rtl" }}>
      <Toolbar>
        <IconButton onClick={closeDrawer}>
          <Icon sx={{ color: "black" }}>chevron_right</Icon>
        </IconButton>
        <Typography variant="h6" sx={{ flexGrow: 1, textAlign: "right" }}>
          مساعد البحث
        </Typography>
      </Toolbar>
      <Divider />

      <Box sx={{ p: 2, height: "calc(100% - 65px)", overflowY: "auto" }}>
        {/* Resources */}
        {/* Pages section */}
        {searchData.ai_answer.resources.length > 0 && (
          <ResourcePagesComponents
            bookInitData={bookInitData}
            searchData={searchData}
            onOpenPdf={onOpenPdf}
          ></ResourcePagesComponents>
        )}

        {/* Accordion for Search Path */}
        {tree_search.length > 0 && (
          <Accordion defaultExpanded>
            <AccordionSummary
              expandIcon={<Icon sx={{ color: "black" }}>expand_more</Icon>}
            >
              <Icon sx={{ color: "black", ml: 1 }}>manage_search</Icon>

              <Box
                display="flex"
                flexDirection="column"
                alignItems="flex-start"
                padding={2}
              >
                <Typography fontWeight="bold">تخصيص نطاق البحث</Typography>
                <Typography variant="caption">
                  {" "}
                  للبحث في هذه الجزئية من الكتاب، اضغط على الزر واكتب سؤالاً
                  أكثر دقة للحصول على المعلومات المطلوبة.
                </Typography>
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Stack spacing={2}>
                {tree_search.map((item) => (
                  <Paper key={item.id} variant="outlined" sx={{ p: { xs: 1.5, sm: 2 } }}>
                    <Stack
                      direction="row"
                      spacing={1}
                      alignItems="center"
                      flexWrap="wrap"
                    >
                      {tree_search
                        .filter((path) => path.level <= item.level)
                        .reverse()
                        .map((pathItem, index) => (
                          <React.Fragment key={pathItem.id}>
                            <PathItem item={pathItem} isLast={index === 0} />
                            {index < item.level && (
                              <Icon sx={{ color: "black" }}>arrow_left</Icon>
                            )}
                          </React.Fragment>
                        ))}
                    </Stack>
                    {item.endPage - item.startPage <=
                      bookInitData.search_range && (
                      <Button
                        variant="contained"
                        onClick={() => handleSearchClick(item)}
                        sx={{
                          mt: 2,
                          bgcolor: "#4069f2ff",
                          "&:hover": { bgcolor: "#0056b3" },
                          borderRadius: 2,
                          width: { xs: "100%", sm: "auto" },
                          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
                        }}
                      >
                        إبحث في جزء: &quot;{item.title}&quot;
                      </Button>
                    )}
                  </Paper>
                ))}
              </Stack>
            </AccordionDetails>
          </Accordion>
        )}

        {/* --- New Section for Relevant Questions --- */}
        {relevant_questions.length > 0 && (
          <Accordion defaultExpanded sx={{ mt: 2 }}>
            <AccordionSummary
              expandIcon={<Icon sx={{ color: "black" }}>expand_more</Icon>}
            >
              <Icon sx={{ color: "black", ml: 1 }}>help_outline</Icon>
              <Typography fontWeight="bold">أسئلة ذات صلة</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Stack spacing={1}>
                {relevant_questions.map((question, index) => (
                  <Button
                    key={index}
                    variant="outlined"
                    fullWidth
                    onClick={() => handleQuestionClick(question)}
                    sx={{
                      justifyContent: "space-between", // Align text to the right
                      textAlign: "right",
                      p: 1.5,
                      fontWeight: "normal",
                      "& .MuiButton-endIcon": {
                        marginRight: 0,
                        marginLeft: 1, // Add margin on the left for RTL
                      },
                    }}
                    endIcon={
                      <Icon sx={{ color: "primary.main" }}>chevron_left</Icon>
                    }
                  >
                    {question}
                  </Button>
                ))}
              </Stack>
            </AccordionDetails>
          </Accordion>
        )}
        {/* --- End New Section --- */}

        {/* Accordion for Similar Topics (commented out) */}
        {similar_search.length > 0 && (
          <Accordion defaultExpanded sx={{ mt: 2 }}>
            <AccordionSummary
              expandIcon={<Icon sx={{ color: "black" }}>expand_more</Icon>}
            >
              <Icon sx={{ color: "black", ml: 1 }}>find_in_page</Icon>
              <Typography fontWeight="bold">
                مواضيع لها علاقة بالسؤال
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Stack spacing={2}>
                {similar_search.map((topic, index) => (
                  <Paper
                    key={index}
                    variant="outlined"
                    sx={{ p: 2, textAlign: "right" }}
                  >
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      &quot;{topic.page_content}&quot;
                    </Typography>
                    <Typography
                      variant="caption"
                      color="text.secondary"
                      display="block"
                    >
                      {topic.book_name} (صفحة: {topic.page_number}
                      {/* Conditional rendering for the book part number */}
                      {topic.book_part_number !== 0
                        ? ` — الجزء: ${topic.book_part_number}`
                        : ""}
                      )
                    </Typography>
                    <Button
                      variant="outlined"
                      onClick={() => handleApiCall(topic, index)}
                      disabled={loading[index]}
                      sx={{
                        mt: 2,
                        flexShrink: 0,
                        ml: { xs: 0, sm: 2 },
                        mb: { xs: 1, sm: 0 },
                        width: { xs: "100%", sm: "auto" },
                        "&:hover": { bgcolor: "#e7f3ff" },
                        borderRadius: 2,
                      }}
                    >
                      {loading[index] ? (
                        <CircularProgress size={24} />
                      ) : (
                        "ما هذا القِسم؟"
                      )}
                    </Button>

                    <Button
                      variant="text"
                      onClick={() => onOpenPdf(bookInitData.books_url[topic.book_part_number], topic.page_number + bookInitData.toc_offset)}
                      disabled={loading[index]}
                      sx={{
                        mt: 1,
                        flexShrink: 0,
                        ml: { xs: 0, sm: 2 },
                        width: { xs: "100%", sm: "auto" },
                        "&:hover": { bgcolor: "#e7f3ff" },
                        borderRadius: 2,
                      }}
                    >
                      {loading[index] ? (
                        <CircularProgress size={24} />
                      ) : (
                        " إذهب إلى الصفحة"
                      )}
                    </Button>
                  </Paper>
                ))}
              </Stack>
            </AccordionDetails>
          </Accordion>
        )}
      </Box>
      <DialogScope
        open={isDialogOpen}
        onClose={() => setIsDialogOpen(false)}
        data={scopeData}
        onSearchSelected={handleSearchClick}
        bookInitData={bookInitData}
      />
    </Box>
  );
};

export default AgentixSearchHelper;
