// Footer.js
/* eslint-disable react/prop-types */
import React from "react";
import {
  Box,
  Container,
  Link,
  Typography,
  Button,
} from "@mui/material";
import { LinkedIn, WhatsApp } from "@mui/icons-material";

const Footer = ({ footerColor = "primary" }) => {
  return (
    <Box
      component="footer"
      dir="ltr"
      sx={{
        py: 6,
        mt: "auto",
        borderTop: "1px solid rgba(0,0,0,0.05)",
        background: footerColor === "primary" ? "#0F172A" : footerColor,
        color: "#000000",
        textAlign: "center",
      }}
    >
      <Container maxWidth="md">
        
        <Typography variant="h4" gutterBottom sx={{ color: "#FF5622", fontWeight: 900, mb: 1 }}>
          Agentix Islam
        </Typography>
        
        <Typography variant="subtitle1" sx={{ color: "#000000", mb: 2, fontWeight: 700 }}>
          A brand of Agentix AI Edtech LTD
        </Typography>

        <Typography variant="body2" sx={{ color: "#475569", mb: 0.5 }}>
          Registered in England and Wales (No: 16187735)
        </Typography>
        <Typography variant="body2" sx={{ color: "#475569", mb: 3 }}>
          24-26, Arcadia Avenue, London, United Kingdom, N3 2JU
        </Typography>

        <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", flexWrap: "wrap", gap: 3, mb: 4 }}>
          <Link
            href="mailto:muwaffaq@theagentixai.com"
            underline="hover"
            sx={{ color: "#FF5622", fontWeight: 600 }}
          >
            muwaffaq@theagentixai.com
          </Link>
          <Typography variant="body1" sx={{ color: "#000000", fontWeight: 600 }}>
            +962781959591
          </Typography>
        </Box>

        <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", gap: 3, mb: 5 }}>
          <Link
            href="https://wa.me/962781959591"
            target="_blank"
            rel="noopener noreferrer"
            sx={{ 
                color: "#FF5622",
                display: "flex",
                transition: "transform 0.2s",
                "&:hover": { transform: "scale(1.15)" }
            }}
          >
            <WhatsApp sx={{ fontSize: 36 }} />
          </Link>
          <Link
            href="https://www.linkedin.com/in/muwaffaqimamai/"
            target="_blank"
            rel="noopener noreferrer"
            sx={{ 
                color: "#FF5622",
                display: "flex",
                transition: "transform 0.2s",
                "&:hover": { transform: "scale(1.15)" }
            }}
          >
            <LinkedIn sx={{ fontSize: 36 }} />
          </Link>
        </Box>

        <Box sx={{ display: "flex", justifyContent: "center", mb: 4 }}>
          <Button
            variant="contained"
            href="https://www.theagentixai.com/"
            target="_blank"
            rel="noopener noreferrer"
            dir="rtl"
            sx={{
              backgroundColor: "#FF5622",
              color: "#fff",
              fontWeight: "bold",
              borderRadius: "50px",
              px: 4,
              py: 1.5,
              fontSize: "1.1rem",
              "&:hover": { backgroundColor: "#E64A19" }
            }}
          >
            صنع بحب من Agentix AI إضغط للتعرف على خدماتنا 
          </Button>
        </Box>

        {/* <Box sx={{ pt: 3, borderTop: "1px solid rgba(0,0,0,0.1)", display: "flex", flexDirection: "column", alignItems: "center", gap: 2 }}>
          <Typography variant="body2" sx={{ color: "#64748B" }}>
            © {new Date().getFullYear()} Agentix Islam – A brand of Agentix AI Edtech LTD – UK. All rights reserved.
          </Typography>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
             <Typography variant="caption" sx={{ color: "#94A3B8", fontWeight: 600 }}>We Accept:</Typography>
             <Box component="img" src="/images/payment/Visa_2021.svg.png" alt="Visa" sx={{ height: 24, width: 'auto', opacity: 0.8 }} />
             <Box component="img" src="/images/payment/mastercasrd.png" alt="Mastercard" sx={{ height: 24, width: 'auto', opacity: 0.8 }} />
          </Box>
        </Box> */}

      </Container>
    </Box>
  );
};

export default Footer;
