import React, { useState, useRef, useEffect } from 'react';
import '../ChatbotPage.css';
import '../CommunityInspector.css';
import { MdChat, MdArrowBack, MdViewList } from 'react-icons/md';
import { Link, useNavigate } from "react-router-dom";

const CommunityInsertRequest = () => {
  

  return (
    <div className="country-selector-page page">
      <div class="chatbot-header">Powered By TOAD</div>
        <div className="header-country">
          <h2>Insert Request</h2>
        </div>

        <div className='menu-inspect'>
          <Link to={"/community-inspector"} className="voceMenuText">
              <div className="voceMenu" id="4">
                <MdArrowBack className="iconaMenu" />
                <span>Go back</span>
              </div>
          </Link>
      </div>
    </div>
  );
};

export default CommunityInsertRequest;
