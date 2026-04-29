import React from "react";
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActionArea,
  Icon,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Fade,
  Zoom,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import Footer from "../Footer";

const themeColors = {
  primary: "#FF5622",
  text: "black",
  backgroundGradient: "linear-gradient(135deg, #4DFFFA, #FFF7AD)",
  glassBg: "rgba(255, 255, 255, 0.4)",
  glassBorder: "1px solid rgba(255, 255, 255, 0.5)",
  glassShadow: "0 8px 32px 0 rgba(31, 38, 135, 0.15)",
  glassBgDarker: "rgba(255, 255, 255, 0.6)",
};

const agents =
[
  {
    "name": "وكيل المذهب الحنفي",
    "title": "Hanafi-AI Agent",
    "description": "أستطيع مساعدتك في فهم مسائل العبادات وتفاصيل الأحكام الفقهية وفق المذهب الحنفي من متن القدوري.",
    "source": "مختصر القدوري",
    "bookId": "Muhktasir_Qudoori_ee17becd-4878-4717-bdcc",
    "icon": "menu_book"
  },
  {
    "title": "Shaf3i-AI Agent",
    "name": "وكيل المذهب الشافعي",
    "description": "أستطيع مساعدتك في تبيان أحكام العبادات والمعاملات واستخراج الفتاوى المعتمدة لدى الشافعية.",
    "source": "بشرى الكريم في مسائل التعليم",
    "bookId": "Bushra_Al_Kareem_58e899a0-1116-47c2-bcee",
    "icon": "auto_stories"
  },
  {
    "name": "وكيل المذاهب الأربعة",
    "title": "Madahb-AI Agent",
    "description": "أستطيع مساعدتك في استعراض الآراء الفقهية المقارنة والبحث الشامل في فقه العبادات والمعاملات.",
    "source": "موسوعة الإمام الزحيلي",
    "bookId": "fiqh_001-123456",
    "icon": "library_books"
  },
  {
    "name": "وكيل الأذكار والأوراد اليومية",
    "title": "Athkar-AI Agent",
    "description": "أستطيع مساعدتك في الوصول إلى الأذكار النبوية الصحيحة والأوراد المأثورة لكل الأوقات والمناسبات.",
    "source": "كتاب الأذكار للنووي",
    "bookId": "Agtx-Azkar_Nawawi-6b24f2abfde641a1a6f89357890dd3b4",
    "icon": "mosque"
  }
]

export default function AgentixIslamLanding() {
  const navigate = useNavigate();

  const handleAgentClick = (bookId) => {
    navigate(`/book/${bookId}`);
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background: themeColors.backgroundGradient,
        direction: "rtl",
        fontFamily: "'Amiri', 'Inter', sans-serif", // Added Amiri for a more authentic Arabic feel if available
        py: 8,
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Decorative background elements to enhance the gradient */}
      <Box
        sx={{
          position: "absolute",
          top: "-10%",
          left: "-10%",
          width: "40%",
          height: "40%",
          background: "radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%)",
          zIndex: 0,
        }}
      />
      <Box
        sx={{
          position: "absolute",
          bottom: "-20%",
          right: "-10%",
          width: "50%",
          height: "50%",
          background: "radial-gradient(circle, rgba(255,255,255,0.6) 0%, rgba(255,255,255,0) 70%)",
          zIndex: 0,
        }}
      />

      <Container maxWidth="lg" sx={{ position: "relative", zIndex: 1 }}>
        {/* Elegant Hero Section with Glassmorphism */}
        <Fade in={true} timeout={1000}>
          <Box
            sx={{
              textAlign: "center",
              mb: 8,
              p: { xs: 4, md: 6 },
              borderRadius: 6,
              background: themeColors.glassBg,
              backdropFilter: "blur(12px)",
              WebkitBackdropFilter: "blur(12px)",
              border: themeColors.glassBorder,
              boxShadow: themeColors.glassShadow,
              position: "relative",
            }}
          >
            {/* Subtle decorative top icon */}
            <Icon sx={{ color: themeColors.primary, fontSize: 48, mb: 2, opacity: 0.8 }}>
              mosque
            </Icon>

            <Typography
              variant="h3"
              component="h1"
              sx={{
                color: themeColors.primary,
                fontWeight: 900,
                mb: 3,
                lineHeight: 1.4,
                fontFamily: "'Tajawal', 'Inter', sans-serif", 
              }}
            >
              إحياء علوم الدين.. برؤية الذكاء الاصطناعي
            </Typography>

            <Typography
              variant="h5"
              sx={{ 
                color: themeColors.text, 
                fontWeight: 600, 
                mb: 2,
                lineHeight: 1.6,
              }}
            >
              حيث وكلاء الذكاء الإصطناعي قادرين على إجابة الفتاوى من مصادر موثوقة 100٪
            </Typography>

            <Typography
              variant="subtitle1"
              sx={{ 
                color: themeColors.text, 
                mt: 1, 
                maxWidth: 850, 
                mx: "auto",
                lineHeight: 1.8,
                opacity: 0.9,
                fontSize: "1.1rem"
              }}
            >
              نضع بين يديك منظومة من الوكلاء الذكيين المتخصصين في العلوم الشرعية، حيث تلتقي التكنولوجيا بوقار المتون العلمية لتقديم إجابات موثوقة بنسبة 100٪ من المصادر الأم.
            </Typography>
          </Box>
        </Fade>

        {/* Agents Grid Section */}
        <Box mb={10}>
          <Box textAlign="center" mb={5}>
            <Typography
              variant="h4"
              sx={{ 
                color: themeColors.primary, 
                fontWeight: 800, 
                mb: 2,
                display: "inline-block",
                borderBottom: `3px solid ${themeColors.primary}`,
                pb: 1
              }}
            >
              بوابة الوكلاء الرقميين
            </Typography>
            <Typography
              variant="h6"
              sx={{ color: themeColors.text, opacity: 0.8 }}
            >
              اختر وكيلك المتخصص حسب المذهب أو الحاجة العلمية
            </Typography>


        <Typography
          variant="caption"
          textAlign="center"
          sx={{ color: themeColors.primary, fontWeight: 800, mb: 5 }}
        >
          إن شاء الله سوف يتم إضافة المزيد من المصادر الموثوقة بالمستقبل
        </Typography>
          </Box>

          <Grid container spacing={4} justifyContent="center">
            {agents.map((agent, index) => (
              <Zoom in={true} style={{ transitionDelay: `${index * 150}ms` }} key={agent.name}>
                <Grid item xs={12} sm={6} md={3}>
                  <Card
                    sx={{
                      height: "100%",
                      borderRadius: 4,
                      background: themeColors.glassBgDarker,
                      backdropFilter: "blur(8px)",
                      border: "1px solid rgba(255,255,255,0.8)",
                      boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
                      transition: "all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
                      display: "flex",
                      flexDirection: "column",
                      overflow: "visible", // To allow icon to pop out slightly
                      "&:hover": {
                        transform: "translateY(-12px) scale(1.02)",
                        boxShadow: `0 20px 40px rgba(255, 86, 34, 0.25)`,
                        background: "rgba(255,255,255,0.9)",
                      },
                    }}
                  >
                    <CardActionArea
                      onClick={() => handleAgentClick(agent.bookId)}
                      sx={{ 
                        height: "100%", 
                        p: 3, 
                        display: "flex", 
                        flexDirection: "column", 
                        alignItems: "center", 
                        justifyContent: "flex-start",
                        textAlign: "center"
                      }}
                    >
                      <Box 
                        sx={{ 
                          width: 80, 
                          height: 80, 
                          borderRadius: "50%", 
                          backgroundColor: "white",
                          display: "flex",
                          justifyContent: "center",
                          alignItems: "center",
                          boxShadow: "0 8px 20px rgba(0,0,0,0.1)",
                          mb: 3,
                          mt: -1,
                          border: `2px solid ${themeColors.primary}`
                        }}
                      >
                        <Icon sx={{ color: themeColors.primary, fontSize: 40 }}>
                          {agent.icon}
                        </Icon>
                      </Box>
                      
                      <CardContent sx={{ p: 0, flexGrow: 1, width: "100%" }}>
                        <Typography
                          variant="h5"
                          sx={{ color: themeColors.primary, fontWeight: 900, mb: 1, letterSpacing: "1px" }}
                        >
                          {agent.name}
                        </Typography>
                        <Typography variant="h6" fontWeight="bold" sx={{ color: themeColors.text, mb: 1 }}>
                          {agent.title}
                        </Typography>
                        <Typography variant="body2" sx={{ color: themeColors.text, mb: 3, opacity: 0.8, minHeight: 40 }}>
                          {agent.description}
                        </Typography>
                        
                        <Box
                          sx={{
                            backgroundColor: "rgba(255, 255, 255, 0.7)",
                            borderTop: `1px solid rgba(255, 86, 34, 0.2)`,
                            p: 2,
                            borderRadius: 3,
                            mt: "auto",
                            width: "100%"
                          }}
                        >
                          <Typography variant="caption" sx={{ color: themeColors.text, display: "block", mb: 0.5, opacity: 0.7 }}>
                            المصدر المعتمد:
                          </Typography>
                          <Typography variant="body1" sx={{ color: themeColors.primary, fontWeight: 800 }}>
                            {agent.source}
                          </Typography>
                        </Box>
                      </CardContent>
                    </CardActionArea>
                  </Card>
                </Grid>
              </Zoom>
            ))}
          </Grid>
        </Box>

        {/* Features Section */}
        <Fade in={true} timeout={1500}>
          <Box
            sx={{
              background: themeColors.glassBg,
              backdropFilter: "blur(10px)",
              border: themeColors.glassBorder,
              borderRadius: 6,
              p: { xs: 3, md: 5 },
              mb: 8,
              boxShadow: themeColors.glassShadow,
            }}
          >
            <Typography
              variant="h4"
              textAlign="center"
              sx={{ color: themeColors.primary, fontWeight: 800, mb: 5 }}
            >
              ما الذي يميز نظامنا؟
            </Typography>
            <Grid container spacing={4}>
              <Grid item xs={12} md={4}>
                <Box textAlign="center">
                  <Box sx={{ bgcolor: "white", width: 64, height: 64, borderRadius: "50%", display: "flex", justifyContent: "center", alignItems: "center", mx: "auto", mb: 2, boxShadow: "0 4px 12px rgba(0,0,0,0.08)" }}>
                    <Icon sx={{ color: themeColors.primary, fontSize: 32 }}>verified</Icon>
                  </Box>
                  <Typography variant="h6" fontWeight="bold" sx={{ color: themeColors.text, mb: 1 }}>هوية فقهية مستقلة</Typography>
                  <Typography variant="body2" sx={{ color: themeColors.text, opacity: 0.8 }}>
                    كل وكيل "تربّى" على متنٍ علمي محدد، مما يمنع اختلاط الأحكام بين المذاهب.
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Box textAlign="center">
                  <Box sx={{ bgcolor: "white", width: 64, height: 64, borderRadius: "50%", display: "flex", justifyContent: "center", alignItems: "center", mx: "auto", mb: 2, boxShadow: "0 4px 12px rgba(0,0,0,0.08)" }}>
                    <Icon sx={{ color: themeColors.primary, fontSize: 32 }}>library_books</Icon>
                  </Box>
                  <Typography variant="h6" fontWeight="bold" sx={{ color: themeColors.text, mb: 1 }}>دقة المصدر</Typography>
                  <Typography variant="body2" sx={{ color: themeColors.text, opacity: 0.8 }}>
                    لا يقوم الذكاء الاصطناعي بالتأليف، بل يستخرج الإجابة من معرفات الكتب الموثقة لدينا.
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Box textAlign="center">
                  <Box sx={{ bgcolor: "white", width: 64, height: 64, borderRadius: "50%", display: "flex", justifyContent: "center", alignItems: "center", mx: "auto", mb: 2, boxShadow: "0 4px 12px rgba(0,0,0,0.08)" }}>
                    <Icon sx={{ color: themeColors.primary, fontSize: 32 }}>search</Icon>
                  </Box>
                  <Typography variant="h6" fontWeight="bold" sx={{ color: themeColors.text, mb: 1 }}>بحث ذكي في الأذكار</Typography>
                  <Typography variant="body2" sx={{ color: themeColors.text, opacity: 0.8 }}>
                    عبر <Box component="span" color={themeColors.primary} fontWeight="bold">Athkar-AI</Box>، يمكنك الوصول إلى الأذكار الصحيحة المأثورة بسهولة فائقة.
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Box>
        </Fade>
      </Container>
      <Footer footerColor="transparent" />
    </Box>
  );
}
