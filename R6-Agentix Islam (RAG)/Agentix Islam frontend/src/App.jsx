/* eslint-disable react/prop-types */
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import AgentixChatBook from './Agentic/UI/AgentixChatBook';
import AgentixIslamLanding from './Agentic/UI/AgentisIslamLanding';
import Login from './Agentic/UI/Login';
import BookSearch from './Agentic/UI/SearcBook';
import { AuthProvider, useAuth } from './context/AuthContext';

function ProtectedRoute({ children }) {
  const { currentUser } = useAuth();
  const location = useLocation();

  if (!currentUser) {
    // Redirect to login page and save the attempted url
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/book/:bookId" element={
            <ProtectedRoute>
              <AgentixChatBook />
            </ProtectedRoute>
          } />
          <Route path="/agentixIslam/BookSearch/:bookId" element={
            <ProtectedRoute>
              <BookSearch />
            </ProtectedRoute>
          } />
          <Route path="/" element={<AgentixIslamLanding />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
