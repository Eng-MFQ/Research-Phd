import React, { useState } from 'react';
import { Box, Button, Typography, Container, Icon, Paper, ThemeProvider, createTheme, CircularProgress } from '@mui/material';
import { signInWithPopup } from 'firebase/auth';
import { auth, provider } from '../../firebase';
import { useNavigate, useLocation } from 'react-router-dom';

const theme = createTheme({
  palette: {
    primary: {
      main: "#FF5622",
    },
    background: {
      default: "linear-gradient(135deg, #4DFFFA, #FFF7AD)",
    },
  },
  typography: {
    fontFamily: "'Tajawal', 'Inter', sans-serif", 
  },
});

export default function Login() {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleGoogleLogin = async () => {
    try {
      setError('');
      setLoading(true);
      await signInWithPopup(auth, provider);
      // Determine where the user came from (e.g. they tried to access a protected book page)
      const from = location.state?.from?.pathname || '/';
      navigate(from, { replace: true });
    } catch (err) {
      setError('حدث خطأ أثناء محاولة تسجيل الدخول');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Box
        sx={{
          minHeight: "100vh",
          background: theme.palette.background.default,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Container maxWidth="sm">
          <Paper
            elevation={3}
            sx={{
              p: 5,
              borderRadius: 4,
              textAlign: 'center',
              backgroundColor: 'rgba(255, 255, 255, 0.8)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255, 255, 255, 0.3)',
            }}
          >
            <Icon sx={{ color: "primary.main", fontSize: 60, mb: 2 }}>account_circle</Icon>
            <Typography variant="h4" fontWeight="bold" color="primary.main" gutterBottom>
              تسجيل الدخول
            </Typography>
            <Typography variant="body1" color="textSecondary" mb={4}>
              الرجاء تسجيل الدخول للوصول إلى الوكلاء ومحرك البحث المتخصص.
            </Typography>

            {error && (
              <Typography color="error" variant="body2" mb={2}>
                {error}
              </Typography>
            )}

            <Button
              variant="contained"
              fullWidth
              size="large"
              onClick={handleGoogleLogin}
              disabled={loading}
              sx={{
                bgcolor: '#ffffff',
                color: '#757575',
                border: '1px solid #ddd',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                '&:hover': {
                  bgcolor: '#f5f5f5',
                  boxShadow: '0 4px 6px rgba(0,0,0,0.15)',
                },
                fontSize: '1rem',
                py: 1.5,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 2,
                borderRadius: 2
              }}
            >
              {loading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                <>
                  <img
                    src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
                    alt="Google Logo"
                    style={{ width: 24, height: 24 }}
                  />
                  المتابعة بحساب جوجل
                </>
              )}
            </Button>
            
            <Button
              variant="text"
              color="primary"
              sx={{ mt: 3 }}
              onClick={() => navigate('/')}
            >
              العودة للصفحة الرئيسية
            </Button>
          </Paper>
        </Container>
      </Box>
    </ThemeProvider>
  );
}
