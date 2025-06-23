import React, { useState, useRef, useEffect } from 'react';
import './ChatbotPage.css';
import './CommunityInspector.css';
import { MdChat, MdDynamicForm, MdViewList } from 'react-icons/md';
import { Link, useNavigate } from "react-router-dom";

const CommunityInspector = () => {
  

  return (
    <div className="country-selector-page page">
      <div class="chatbot-header">Powered By TOAD</div>
        <div className="header-country">
          <h2>Community Inspector</h2>
        </div>

        <div className='menu-inspect'>
          <Link to={"/community-insert-requests"} className="voceMenuText">
              <div className="voceMenu">
                <MdDynamicForm className="iconaMenu" />
                <span>Insert request</span>
              </div>
          </Link>

          <Link to={"/community-requests"} className="voceMenuText">
              <div className="voceMenu">
                <MdViewList className="iconaMenu" />
                <span>View Community requests</span>
              </div>
          </Link>
      </div>
    </div>
  );
};

export default CommunityInspector;
