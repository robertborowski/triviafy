class NavbarCandidatesNotSignedInClass extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    console.log(this.getAttribute("slack_state_uuid_js"));
  }

  connectedCallback() {
    this.innerHTML = 
`
<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Top Shadow START -->
<div class="navbar-2-outline-shadow default-box-shadow-grey-reg">
  <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Top Shadow END -->
  
  <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Entire START -->
  <nav class="navbar-2-not-signed-in">
    
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Logo and Name START -->
    <div class="navbar-2-logo-and-name-section">
      <a href="${this.getAttribute("link_home_js")}"><img src="/static/images/logo/Logo.png" alt="Triviafy Logo" class="navbar-2-not-signed-in-logo"></a>
      <div class="brand-title-2-not-signed-in"><a href="${this.getAttribute("link_home_js")}">Triviafy</a></div>
    </div>
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Logo and Name END -->


    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Hamburger Toggle START -->
    <a href="#" class="toggle-button-2">
      <span class="toggle-bar-2"></span>
      <span class="toggle-bar-2"></span>
      <span class="toggle-bar-2"></span>
    </a>
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Hamburger Toggle END -->


    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 1 - START -->
    <div class="navbar-links-2-not-signed-in">
      <ul>
        <li class="navbar-list-item-2"><a href="#">Resources <i class="fas fa-angle-down navbar-drop-down-arrow-2"></i></a>
          <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - START -->
          <ul class="links-level-2 default-box-shadow-grey-reg">
            <li><a href="${this.getAttribute("link_faq_js")}"><i class="fas fa-question-circle font-awesome-icon"></i>FAQ</a></li>
            <li><a href="${this.getAttribute("link_about_js")}"><i class="fas fa-puzzle-piece font-awesome-icon"></i>About</a></li>
            <li><a href="${this.getAttribute("link_privacy_js")}"><i class="fas fa-lock font-awesome-icon"></i>Privacy</a></li>
            <li><a href="${this.getAttribute("link_blog_js")}"><i class="fas fa-pen-square font-awesome-icon"></i>Blog</a></li>
          </ul>
          <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - END -->
        </li>
        <li class="navbar-list-item-1"><a href="#">Test library</a></li>
        <li class="navbar-list-item-4"><a href="#">Login</a>
        </li>
        <div class="navbar-not-signed-in-demo-button-section">
          <a href="${this.getAttribute("link_demo_js")}"><button class="default-button-format default-button-format-primary-color navbar-not-signed-in-button-position">Try for free!</button></a>
        </div>
      </ul>
    </div>
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 1 - END -->
    
  </nav>

</div>
<div class="spacer-navbar-not-signed-in-2"></div>
<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Entire END -->   
`;
  }
}

customElements.define('nav-candidates-not-signed-in-component', NavbarCandidatesNotSignedInClass);