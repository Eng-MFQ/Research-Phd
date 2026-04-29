import React, { useState } from "react";
import {
  Container,
  Typography,
  Card,
  CardContent,
  Button,
  Box,
  Snackbar,
  Alert,
  List,
  ListItem,
} from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";

// Main App component
const AthkarHelper = () => {
  const [copiedIndex, setCopiedIndex] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);

  // Data for the supplications
  const adkarsData = [
    {
      category: "أدعية الاستيقاظ والنوم",
      items: [
        { id: 1, text: "ماذا أقول عند الاستيقاظ من النوم؟" },
        { id: 2, text: "ماذا أقول عند لبس الثوب الجديد؟" },
        { id: 3, text: "ماذا أقول عند الخروج من المنزل؟" },
        { id: 4, text: "ماذا أقول عند دخول المنزل؟" },
        { id: 5, text: "ماذا أقول عند القلق من الأرق؟" },
        { id: 6, text: "ماذا أقول عند الفزع من المنام؟" },
      ],
    },
    {
      category: "أدعية الصلاة والمساجد",
      items: [
        { id: 7, text: "ماذا أقول عند دخول المسجد؟" },
        { id: 8, text: "ماذا أقول عند الخروج من المسجد؟" },
        { id: 9, text: "ماذا أقول في دعاء الاستفتاح بالصلاة؟" },
        { id: 10, text: "ماذا أقول في دعاء بعد التشهد الأخير؟" },
        { id: 11, text: "ماذا أقول في الأذكار بعد الصلاة؟" },
      ],
    },
    {
      category: "أدعية اليوم والليلة",
      items: [
        { id: 12, text: "ماذا أقول في أذكار الصباح والمساء؟" },
        { id: 13, text: "ماذا أقول عند رؤية الهلال؟" },
        { id: 14, text: "ماذا أقول عند الإفطار من الصيام؟" },
      ],
    },
    {
      category: "أدعية السفر والمركبات",
      items: [
        { id: 15, text: "ماذا أقول في دعاء الركوب؟" },
        { id: 16, text: "ماذا أقول في دعاء السفر؟" },
        { id: 17, text: "ماذا أقول عند الرجوع من السفر؟" },
        { id: 18, text: "ماذا أقول عند دخول قرية؟" },
        { id: 19, text: "ماذا أقول عند نزول منزل؟" },
      ],
    },
    {
      category: "أدعية الحياة اليومية والمواقف المختلفة",
      items: [
        { id: 20, text: "ماذا أقول في دعاء القلق والحزن؟" },
        { id: 21, text: "ماذا أقول في دعاء الكرب؟" },
        { id: 22, text: "ماذا أقول في دعاء الاستخارة؟" },
        { id: 23, text: "ماذا أقول عند سماع الرعد؟" },
        { id: 24, text: "ماذا أقول عند نزول المطر؟" },
        { id: 25, text: "ماذا أقول عند رؤية الحريق؟" },
        { id: 26, text: "ماذا أقول عند الشعور بالغضب؟" },
        { id: 27, text: "ماذا أقول عند رؤية شخص مبتلى؟" },
        { id: 28, text: "ماذا أقول لمن أصابه دين؟" },
        { id: 29, text: "ماذا أقول عند رؤية ما يُعجب به؟" },
        { id: 30, text: "ماذا أقول عند زيارة القبور؟" },
      ],
    },
  ];

  // Function to handle the copy action
  const handleCopy = async (text, index) => {
    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(text);
      } else {
        // Fallback for older browsers
        const textarea = document.createElement("textarea");
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
      }
      setCopiedIndex(index);
      setOpenSnackbar(true);
      setTimeout(() => setCopiedIndex(null), 2000); // Reset the notification after 2 seconds
    } catch (err) {
      console.error("Failed to copy text: ", err);
    }
  };

  const handleCloseSnackbar = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }
    setOpenSnackbar(false);
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography
        variant="h3"
        component="h1"
        align="center"
        sx={{ fontWeight: "bold", color: "primary.main", mb: 4 }}
      >
        أدعية و أذكار
      </Typography>

      {adkarsData.map((categoryData, catIndex) => (
        <Card
          dir="rtl"
          key={catIndex}
          sx={{ mb: 3, borderRadius: 2, boxShadow: 3 }}
        >
          <CardContent dir="rtl">
            <Typography
              variant="h5"
              component="h2"
              sx={{ fontWeight: "semibold", color: "primary.main", mb: 2 }}
            >
              {categoryData.category}
            </Typography>
            <List>
              {categoryData.items.map((item, itemIndex) => (
                <ListItem
                  key={item.id}
                  sx={{ bgcolor: "grey.50", borderRadius: 2, mb: 1, p: 2 }}
                >
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-evenly",

                      width: "100%",
                      flexDirection: { xs: "column", sm: "row" },
                    }}
                  >
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() =>
                        handleCopy(item.text, `${catIndex}-${itemIndex}`)
                      }
                      sx={{ borderRadius: 8 }}
                    >
                      نسخ
                    </Button>
                    <Typography sx={{ flexGrow: 1, mb: { xs: 1, sm: 0 } }}>
                      {item.text}
                    </Typography>
                  </Box>
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      ))}

      <Snackbar
        open={openSnackbar}
        autoHideDuration={2000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity="success"
          sx={{ width: "100%" }}
        >
          <Typography color="black">تم النسخ!</Typography>
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default AthkarHelper;
