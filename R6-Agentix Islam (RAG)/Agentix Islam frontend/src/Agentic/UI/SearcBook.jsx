import React, { useEffect, useState } from "react";
import {
  Box,
  Container,
  TextField,
  Button,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Stack,
  ThemeProvider,
  createTheme,
  CssBaseline,
  InputAdornment,
  List,
  ListItem,
  Icon,
} from "@mui/material";
import { Search, LibraryBooks } from "@mui/icons-material";
import { CacheProvider } from "@emotion/react";
import createCache from "@emotion/cache";
import { prefixer } from "stylis";
import rtlPlugin from "stylis-plugin-rtl";
import { apiUrl } from "../../api";
import { useParams } from "react-router-dom";
import PdfViewerDialog from "./PdfViewerDialog";

const theme = createTheme({
  palette: {
    primary: {
      main: "#FF5622",
    },
    text: {
      primary: "#000000",
    },
    background: {
      default: "#f9fafb",
      paper: "#ffffff",
    },
  },
  typography: {
    fontFamily: "Inter, sans-serif",
  },
});

// Create a custom MUI cache to handle RTL
const cacheRtl = createCache({
  key: "muirtl",
  stylisPlugins: [prefixer, rtlPlugin],
});

export default function BookSearch() {
  const [query, setQuery] = useState("");
  const [limit, setLimit] = useState(10); // Changed from numResults to limit
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { bookId } = useParams();
  const [bookInitData, setBookInitData] = useState(null);
  const [isInitializing, setIsInitializing] = useState(true);
  const [initError, setInitError] = useState(false);

  // PDF Viewer State
  const [pdfViewerOpen, setPdfViewerOpen] = useState(false);
  const [pdfViewerUrl, setPdfViewerUrl] = useState("");
  const [pdfViewerPage, setPdfViewerPage] = useState(1);

  const handleOpenPdf = (fileUrl, pageNumber) => {
    setPdfViewerUrl(fileUrl);
    setPdfViewerPage(pageNumber);
    setPdfViewerOpen(true);
  };

  useEffect(() => {
    const initChat = async () => {
      setIsInitializing(true);
      setInitError(false);
      console.log(`Initializing chat for book ID: ${bookId}`);

      if (!bookId) {
        setInitError(true);
        setIsInitializing(false);
        return;
      }

      try {
        const response = await fetch(`${apiUrl}/book/chat/init/`, {
          method: "POST", // Changed from 'GET' to 'POST'
          headers: {
            "Content-Type": "application/json",
            accept: "application/json",
          },
          body: JSON.stringify({
            // Sending book_id in the request body
            book_id: bookId,
          }),
        });

        console.log(response.body);
        if (!response.ok) {
          throw new Error("Book not found or API error");
        }

        const initData = await response.json();
        setBookInitData(initData);
        console.log("Initial data:", initData);
      } catch (err) {
        console.error("Initial API call failed:", err);
        setInitError(true);
      } finally {
        setIsInitializing(false);
      }
    };

    initChat();
  }, [bookId]);

  // Function to fetch data from the API
  const fetchData = async () => {
    if (!query) {
      setResults([]);
      setError("الرجاء إدخال عبارة البحث.");
      return;
    }

    setLoading(true);
    setError(null);

    // Encode the query for the URL
    const encodedQuery = encodeURIComponent(query);
    const url = `${apiUrl}/book/${bookId}/${encodedQuery}/${limit}`; // Updated API endpoint

    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("حدث خطأ في جلب البيانات من الخادم.");
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      console.error("Failed to fetch:", err);
      setError("عذراً، حدث خطأ. يرجى المحاولة مرة أخرى.");
    } finally {
      setLoading(false);
    }
  };

  if (isInitializing) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            height: "100vh",
            background: theme.palette.background.default,
          }}
        >
          <CircularProgress color="primary" sx={{ mb: 2 }} />
          <Typography color="black" variant="h6">
            يتم التواصل مع الكتاب...
          </Typography>
        </Box>
      </ThemeProvider>
    );
  }

  if (initError) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            height: "100vh",
            background: theme.palette.background.default,
          }}
        >
          <Icon color="error" sx={{ fontSize: 60, mb: 2 }}>
            error_outline
          </Icon>
          <Typography variant="h5" color="error" sx={{ mb: 1 }}>
            الكتاب غير موجود
          </Typography>
          <Typography variant="body1" color="text.secondary">
            يرجى التأكد من أن الكتاب صحيح.
          </Typography>
        </Box>
      </ThemeProvider>
    );
  }

  return (
    <CacheProvider value={cacheRtl}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Container maxWidth="md" sx={{ py: 4 }}>
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 3,
              direction: "rtl",
              textAlign: "right",
            }}
          >
            <Box
              sx={{
                width: "100%",
                p: 3,
                borderRadius: 4,
                backgroundColor: "background.paper",
                boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 2,
              }}
            >
              <Typography
                variant="h4"
                component="h1"
                align="center"
                gutterBottom
                sx={{ color: "primary.main" }}
              >
                البحث السريع {<br />}
                في {bookInitData ? bookInitData.book_name : "الكتاب"}
              </Typography>
              <Typography variant="body1" align="center" color="text.secondary">
                إبحث في محتوى الكتب حسب عبارة معينة.
              </Typography>
              <Stack
                direction={{ xs: "column", sm: "row" }}
                spacing={2}
                sx={{ width: "100%", alignItems: "center" }}
              >
                {/* Search Query TextField */}
                <TextField
                  fullWidth
                  label="أدخل عبارة البحث"
                  variant="outlined"
                  helperText="بإمكانك البحث عن كلمة أو جملة بأي لغة تريد"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <Search color="primary" />
                      </InputAdornment>
                    ),
                    // Ensures text starts from the right within the input field
                    inputProps: {
                      style: { textAlign: "right" },
                    },
                  }}
                  sx={{
                    flexGrow: 1,
                    // Ensures the component respects the RTL environment
                    direction: "rtl",
                  }}
                />

                {/* Results Limit TextField (Updated max limit to 30) */}
                <TextField
                  label="عدد النتائج"
                  variant="outlined"
                  type="number"
                  value={limit}
                  helperText="الحد الأقصى 30"
                  onChange={(e) =>
                    setLimit(Math.min(30, Math.max(1, +e.target.value)))
                  }
                  inputProps={{
                    min: 1,
                    max: 30, // <<< CHANGED: Limit is now 30
                    style: { textAlign: "right" }, // <<< ADDED: Ensures text starts from the right
                  }}
                  sx={{
                    width: { xs: "100%", sm: 150 },
                    direction: "rtl", // Ensures the component respects the RTL environment
                  }}
                />

                <Button
                  variant="contained"
                  color="primary"
                  onClick={fetchData}
                  sx={{
                    width: { xs: "100%", sm: "auto" },
                    height: "56px",
                    fontSize: "1rem",
                  }}
                >
                  بحث
                </Button>
              </Stack>
            </Box>

            {loading && (
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "center",
                  p: 4,
                  width: "100%",
                }}
              >
                <CircularProgress color="primary" />
              </Box>
            )}

            {error && (
              <Box
                sx={{
                  p: 2,
                  backgroundColor: "error.main",
                  color: "white",
                  borderRadius: 2,
                  textAlign: "center",
                }}
              >
                <Typography variant="body1">{error}</Typography>
              </Box>
            )}

            {!loading && results.length > 0 && (
              <List
                sx={{
                  width: "100%",
                  display: "flex",
                  flexDirection: "column",
                  gap: 2,
                }}
              >
                {results.map((result, index) => (
                  <ListItem key={index} disablePadding>
                    <Card sx={{ width: "100%" }}>
                      <CardContent>
                        <Stack
                          direction={{ xs: "column", sm: "row" }}
                          spacing={3}
                          justifyContent="space-between"
                          alignItems={{ xs: "flex-start", sm: "center" }}
                          flexWrap="wrap"
                          mb={2}
                        >
                          <Button
                            variant="contained"
                            onClick={() => handleOpenPdf(bookInitData.books_url[result.book_part_number], result.page_number + bookInitData.toc_offset)}
                            sx={{
                              p: 1,
                              px: 2,
                              borderRadius: 2,
                              whiteSpace: "nowrap",
                              minWidth: "fit-content",
                            }}
                          >
                            الذهاب إلى الصفحة
                          </Button>
                          <Typography
                            variant="subtitle1"
                            component="span"
                            sx={{
                              color: "primary.main",
                              flexGrow: 1,
                            }}
                          >
                            من: {result.book_name}— صفحة: {result.page_number}
                          </Typography>
                        </Stack>
                        <Typography variant="body1" component="p">
                          {result.page_content}
                        </Typography>
                      </CardContent>
                    </Card>
                  </ListItem>
                ))}
              </List>
            )}

            {!loading && !error && results.length === 0 && query && (
              <Box
                sx={{
                  p: 4,
                  backgroundColor: "background.paper",
                  borderRadius: 2,
                  width: "100%",
                  textAlign: "center",
                }}
              >
                <Typography variant="h6" color="text.secondary">
                  لا توجد نتائج مطابقة لبحثك.
                </Typography>
              </Box>
            )}

            {!loading && !error && results.length === 0 && !query && (
              <Box
                sx={{
                  p: 4,
                  backgroundColor: "background.paper",
                  borderRadius: 2,
                  width: "100%",
                  textAlign: "center",
                }}
              >
                <Typography
                  variant="h6"
                  color="text.secondary"
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: 1,
                  }}
                >
                  <LibraryBooks />
                  ابدأ بالبحث في موسوعة الفقه الإسلامي.
                </Typography>
              </Box>
            )}
          </Box>
        </Container>

        {/* PDF Viewer Dialog */}
        <PdfViewerDialog
          open={pdfViewerOpen}
          onClose={() => setPdfViewerOpen(false)}
          fileUrl={pdfViewerUrl}
          initialPage={pdfViewerPage}
        />
      </ThemeProvider>
    </CacheProvider>
  );
}
