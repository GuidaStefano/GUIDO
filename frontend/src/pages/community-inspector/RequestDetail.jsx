import React, { useState, useRef, useEffect } from 'react';
import '../ChatbotPage.css';
import '../CommunityInspector.css';
import { MdChat, MdArrowBack, MdViewList } from 'react-icons/md';
import { Link, useNavigate } from "react-router-dom";
import CommunityGraph from '../../components/CommunityGraph';

const RequestDetail = () => {
  

  return (
    <div className="country-selector-page page">      
        <div className=''>
          <Link to={"/community-inspector"} className="voceMenuText">
              <div className="voceMenu floating-back" id="4">
                <MdArrowBack className="iconaMenu" />
                <span>Go back</span>
              </div>
          </Link>
        </div>
        <CommunityGraph></CommunityGraph>
    </div>
  );
};

export default RequestDetail;
