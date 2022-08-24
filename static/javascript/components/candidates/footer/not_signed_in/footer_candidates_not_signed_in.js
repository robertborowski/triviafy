class FooterNotSignedInClassCandidates extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    // console.log(this.getAttribute("link_home"));
  }

  connectedCallback() {
    this.innerHTML = 
`
<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer All - START -->
<footer class="footer-not-signed-in-3-background-color">
  <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer Top - START -->
  <div class="footer-not-signed-in-3-section-top">
    
    <div class="footer-not-signed-in-3-sub-section">
      <p class="footer-title-3 footer-title-position-3">Triviafy Candidates</p>
      <div class="footer-logo-container-3">
        <a href="${this.getAttribute("link_home_js")}"><img src="/static/images/logo/Logo.png" alt="logo" class="footer-logo-img-3"></a>
      </div>
    </div>

    <div class="footer-not-signed-in-3-sub-section">
      <p class="footer-title-3 footer-title-position-3">Resources</p>
      <ul class="footer-not-signed-in-3-ul">
        <li class="footer-sub-title-item-3 footer-sub-title-item-position-3"><a href="${this.getAttribute("link_candidates_about_js")}" class="footer-a-3">About</a></li>
        <li class="footer-sub-title-item-3 footer-sub-title-item-position-3"><a href="${this.getAttribute("link_candidates_faq_js")}" class="footer-a-3">FAQ</a></li>
        <li class="footer-sub-title-item-3 footer-sub-title-item-position-3"><a href="#" class="footer-a-3">Pricing</a></li>
        <li class="footer-sub-title-item-3 footer-sub-title-item-position-3"><a href="#" class="footer-a-3">Login</a></li>
        <li class="footer-sub-title-item-3 footer-sub-title-item-position-3"><a href="#" class="footer-a-3">Create Account</a></li>
      </ul>
    </div>

    <div class="footer-not-signed-in-3-sub-section">
      <p class="footer-title-3 footer-title-position-3">Legal</p>
      <ul class="footer-not-signed-in-3-ul">
        <li class="footer-sub-title-item-3 footer-sub-title-item-position-3"><a href="${this.getAttribute("link_privacy_js")}" class="footer-a-3">Privacy</a></li>
        <li class="footer-sub-title-item-3 footer-sub-title-item-position-3"><a href="${this.getAttribute("link_terms_conditions_js")}" class="footer-a-3">Terms of Service</a></li>
      </ul>
    </div>
  </div>
  <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer Top - END -->

  
  <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer Bottom - START -->
  <div class="footer-not-signed-in-3-section-bottom">
    <div class="footer-not-signed-in-3-sub-section-bottom">
      <p class="footer-copyright-2">©2022 Triviafy | All Rights Reserved.</p>
    </div>


    <div class="footer-not-signed-in-3-sub-section-bottom">
      <p class="footer-copyright-2">Contact: Robert@Triviafy.com</p>
    </div>
    
    <div class="footer-not-signed-in-3-sub-section-bottom">
      <a href="https://twitter.com/TriviafyWork" class="footer-social-logo-3" target="_blank"><i class="fab fa-twitter-square"></i></a>
      <a href="https://www.linkedin.com/company/triviafy" class="footer-social-logo" target="_blank"><i class="fab fa-linkedin"></i></a>
    </div>
  </div>
  <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer Bottom - END -->
</footer>
<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer All - END -->
`;
  }
}

customElements.define('footer-candidates-not-signed-in-component', FooterNotSignedInClassCandidates); 