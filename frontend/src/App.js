// src/App.js
import React, { useState, useEffect } from 'react';
import './App.css';
import AppShell from "./AppShell";
import Menu from "./components/menu";

import {
  BrowserRouter,
  Navigate,
  Outlet,
  Route,
  Routes,
  redirect
} from "react-router-dom";
import CountrySelector from './pages/CountrySelector';
import ChatbotPage from './pages/ChatbotPage';
import menu from "./components/menu";
import CommunityInspector from './pages/CommunityInspector';
import CommunityRequests from './pages/community-inspector/CommunityRequests';
import CommunityInsertRequest from './pages/community-inspector/CommunityInsertRequest';
import RequestDetail from './pages/community-inspector/RequestDetail';

const AppRoutes = () =>{
    return (
        <Routes>
            <Route path="/" element={<AppShell> <Menu/> <CountrySelector/> </AppShell> }/>
            <Route path="/chatbot" element={<AppShell> <Menu/><ChatbotPage/> </AppShell>}/>
            <Route path="/community-inspector" element={<AppShell> <Menu/><CommunityInspector/> </AppShell>}/>
            <Route path="/community-requests" element={<AppShell> <Menu/><CommunityRequests/> </AppShell>}/>
            <Route path="/community-insert-requests" element={<AppShell> <Menu/><CommunityInsertRequest/> </AppShell>}/>
            <Route path="/request-detail" element={<AppShell> <Menu/><RequestDetail/> </AppShell>}/>
        </Routes>
    )
}


const App = () => {
  return (
    <div className="contenitorePaginaHomePage">
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>

    </div>
  );
};

export default App;
