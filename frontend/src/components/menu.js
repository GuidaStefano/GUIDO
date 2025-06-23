import React from "react";
import "./menu_style.css";
import { Link, useNavigate } from "react-router-dom";
import { MdChat, MdPlace, MdHandshake } from 'react-icons/md';
import logoPath from "../images/GUIDO_logo.svg";

function addClassActive(id) {
  const attualmenteSelezionato = document.querySelectorAll(".voceMenuActive");
  attualmenteSelezionato.forEach(el => el.classList.remove("voceMenuActive"));
  document.getElementById(id).classList.add("voceMenuActive");
}

function Menu() {
  const nav = useNavigate();

  return (
    <div className="contenitoreMenu shadow">
      <div className="logoContainer">
        <img src={logoPath} alt="GUiDO Logo" className="logoMenu" />
      </div>

      <nav className="contenitoreVociMenu">
        <Link to={"/"} className="voceMenuText" onClick={() => addClassActive(2)}>
          <div className="voceMenu voceMenuActive" id="2">
            <MdPlace className="iconaMenu" />
            <span>Culture Inspector</span>
          </div>
        </Link>

        <Link to={"/chatbot"} className="voceMenuText" onClick={() => addClassActive(1)}>
          <div className="voceMenu" id="1">
            <MdChat className="iconaMenu" />
            <span>Chatbot</span>
          </div>
        </Link>

        <Link to={"/community-inspector"} className="voceMenuText" onClick={() => addClassActive(3)}>
          <div className="voceMenu" id="3">
            <MdHandshake className="iconaMenu" />
            <span>Community Inspector</span>
          </div>
        </Link>
      </nav>
    </div>
  );
}

export default Menu;
