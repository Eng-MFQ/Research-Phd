import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  IconButton,
  Box,
  Typography,
  Stack,
  Button,
  CircularProgress,
  useMediaQuery,
  useTheme,
  Icon,
} from "@mui/material";
import { Document, Page, pdfjs } from "react-pdf";

// Ensure worker is configured for React-PDF to parse documents
// Using the recommended setup for Vite + react-pdf v9+
pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

const PdfViewerDialog = ({ open, onClose, fileUrl, initialPage = 1 }) => {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(initialPage);
  const [scale, setScale] = useState(1.0);
  const [loading, setLoading] = useState(true);
  const [pdfError, setPdfError] = useState(null);

  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down("md"));

  // Reset states when a new file or starting page is provided
  useEffect(() => {
    if (open) {
      setPageNumber(initialPage);
      setScale(1.0); // Reset scale on open
      setLoading(true); // show generic loader initially
    }
  }, [open, fileUrl, initialPage]);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
    setLoading(false);
  }

  // Handle Zoom In
  const handleZoomIn = () => {
    setScale((prevScale) => Math.min(prevScale + 0.25, 3.0)); // Max scale 3x
  };

  // Handle Zoom Out
  const handleZoomOut = () => {
    setScale((prevScale) => Math.max(prevScale - 0.25, 0.5)); // Min scale 0.5x
  };

  // Navigate to previous page
  const prevPage = () => {
    setPageNumber((prev) => Math.max(prev - 1, 1));
  };

  // Navigate to next page
  const nextPage = () => {
    setPageNumber((prev) => Math.min(prev + 1, numPages || 1));
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullScreen={fullScreen}
      maxWidth="md"
      fullWidth
      sx={{ direction: "ltr" }} // Force LTR for the PDF viewer layout if needed, though RTL text inside might be okay. Keeps controls standard.
    >
      <DialogTitle
        sx={{
          m: 0,
          p: 2,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          bgcolor: "background.paper",
          direction: "rtl", // Title in RTL
        }}
      >
        <Typography variant="h6" fontWeight="bold">
          عارض المستندات
        </Typography>
        <IconButton
          aria-label="close"
          onClick={onClose}
         
        >
          <Icon  sx={{
            color: "black",
          }}>close</Icon>
        </IconButton>
      </DialogTitle>
      
      {/* Controls Bar */}
      <Box
        sx={{
          bgcolor: "#f5f5f5",
          py: 1,
          px: { xs: 1, sm: 2 },
          display: "flex",
          justifyContent: { xs: "center", sm: "space-between" },
          alignItems: "center",
          borderBottom: "1px solid #e0e0e0",
          flexWrap: "wrap",
          gap: 1
        }}
      >
        {/* Zoom Controls */}
        <Stack direction="row" spacing={1} alignItems="center">
          <IconButton onClick={handleZoomOut} disabled={scale <= 0.5} size="small" aria-label="zoom out">
            <Icon sx={{ color: scale <= 0.5 ? "text.disabled" : "error.main" }}>zoom_out</Icon>
          </IconButton>
          <Typography variant="body2" sx={{ fontWeight: 'bold' }}>{Math.round(scale * 100)}%</Typography>
          <IconButton onClick={handleZoomIn} disabled={scale >= 3.0} size="small" aria-label="zoom in">
            <Icon sx={{ color: scale >= 3.0 ? "text.disabled" : "success.main" }}>zoom_in</Icon>
          </IconButton>
        </Stack>

        {/* Pagination Controls */}
        <Stack direction="row" spacing={1} alignItems="center">
          <Button
            size="small"
            variant="outlined"
            onClick={prevPage}
            disabled={pageNumber <= 1}
            startIcon={<Icon sx={{ color: pageNumber <= 1 ? "text.disabled" : "primary.main" }}>chevron_left</Icon>}
          >
            السابق
          </Button>
          <Typography variant="body2" sx={{ minWidth: "80px", textAlign: "center", fontWeight: 'bold' }}>
            {pageNumber} / {numPages || "--"}
          </Typography>
          <Button
            size="small"
            variant="outlined"
            onClick={nextPage}
            disabled={pageNumber >= numPages}
            endIcon={<Icon sx={{ color: pageNumber >= numPages ? "text.disabled" : "primary.main" }}>chevron_right</Icon>}
          >
            التالي
          </Button>
        </Stack>

        {/* Open in New Tab Button */}
        <Button
          size="small"
          variant="contained"
          onClick={() => window.open(`${fileUrl}#page=${pageNumber}`, '_blank')}
          startIcon={<Icon sx={{ color: "white" }}>open_in_new</Icon>}
          sx={{
            bgcolor: "info.main",
            "&:hover": { bgcolor: "info.dark" },
            boxShadow: 2,
          }}
        >
          فتح في تبويب جديد
        </Button>
      </Box>

      {/* PDF Content */}
      <DialogContent dividers sx={{ p: 0, bgcolor: "#e0e0e0", display: "flex", justifyContent: "center", overflow: "auto" }}>
        {open && fileUrl && (
          <Box sx={{ p: 2 }}>
            <Document
              file={fileUrl}
              onLoadSuccess={onDocumentLoadSuccess}
              onLoadError={(error) => {
                console.error("Error loading PDF:", error);
                setPdfError(error.message || "Unknown error occurred");
                setLoading(false);
              }}
              loading={
                <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", p: 4, height: 400 }}>
                  <CircularProgress />
                </Box>
              }
              error={
                <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", p: 4, color: "error.main" }}>
                  <Icon sx={{ fontSize: 40, mb: 1 }}>error_outline</Icon>
                  <Typography>عذراً، تعذر تحميل المستند.</Typography>
                  {pdfError && (
                    <Typography variant="caption" sx={{ mt: 1, direction: "ltr" }}>
                      Error details: {pdfError}
                    </Typography>
                  )}
                  <Button 
                    variant="outlined" 
                    color="error" 
                    sx={{ mt: 2 }} 
                    onClick={() => window.open(`${fileUrl}#page=${pageNumber}`, '_blank')}
                  >
                    فتح في تبويب جديد المحاولة
                  </Button>
                </Box>
              }
            >
              <Page
                pageNumber={pageNumber}
                scale={scale}
                width={fullScreen ? window.innerWidth - 32 : undefined}
                renderTextLayer={false}
                renderAnnotationLayer={false}
                loading={
                  <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", height: 400 * scale }}>
                    <CircularProgress />
                  </Box>
                }
                className="pdf-page-container" 
              />
            </Document>
          </Box>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default PdfViewerDialog;
