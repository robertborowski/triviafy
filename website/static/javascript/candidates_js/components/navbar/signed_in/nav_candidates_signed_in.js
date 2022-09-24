class NavbarCandidatesSignedInClass extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    // console.log(this.getAttribute("slack_state_uuid_js"));
  }

  connectedCallback() {
    this.innerHTML = 
`
<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Top Shadow START -->
<div class="navbar-3-outline-shadow default-box-shadow-grey-reg">
  <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Top Shadow END -->
  
  <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Entire START -->
  <nav class="navbar-3-not-signed-in">
    
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Logo and Name START -->
    <div class="navbar-3-logo-and-name-section">
      <a href="${this.getAttribute("link_home_js")}"><img src="/static/images/candidates/logo/Logo.png" alt="Triviafy Logo" class="navbar-3-not-signed-in-logo"></a>
      <div class="brand-title-3-not-signed-in"><a href="${this.getAttribute("link_home_js")}">Triviafy</a></div>
    </div>
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Logo and Name END -->


    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Hamburger Toggle START -->
    <a href="#" class="toggle-button-3">
      <span class="toggle-bar-3"></span>
      <span class="toggle-bar-3"></span>
      <span class="toggle-bar-3"></span>
    </a>
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Hamburger Toggle END -->


    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 1 - START -->
    <div class="navbar-links-3-not-signed-in">
      <ul>
        <li class="navbar-list-item-a"><a href="#">Candidates <i class="fas fa-angle-down navbar-drop-down-arrow-a"></i></a>
          <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - START -->
          <ul class="links-level-2 default-box-shadow-grey-reg">
            <li><a href="#">Candidates1</a></li>
            <li><a href="#">Candidates2</a></li>
            <li><a href="#">Candidates3</a></li>
          </ul>
          <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - END -->
        </li>
        
        <li class="navbar-list-item-a"><a href="#">Assessments <i class="fas fa-angle-down navbar-drop-down-arrow-a"></i></a>
          <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - START -->
          <ul class="links-level-2 default-box-shadow-grey-reg">
            <li><a href="#">Assessments1</a></li>
            <li><a href="#">Assessments2</a></li>
            <li><a href="#">Assessments3</a></li>
          </ul>
          <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - END -->
        </li>
        
        <li class="navbar-list-item-a"><a href="#">Account <i class="fas fa-angle-down navbar-drop-down-arrow-a"></i></a>
          <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - START -->
          <ul class="links-level-2 default-box-shadow-grey-reg">
            <li><a href="#">Account1</a></li>
            <li><a href="#">Account2</a></li>
            <li><a href="#">Account3</a></li>
          </ul>
          <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - END -->
        </li>
      </ul>
    </div>
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 1 - END -->
    
  </nav>

</div>
<div class="spacer-navbar-not-signed-in-3"></div>
<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Entire END -->
`;
  }
}

customElements.define('nav-candidates-signed-in-component', NavbarCandidatesSignedInClass);