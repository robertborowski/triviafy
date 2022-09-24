class FooterSignedInClassCandidates extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    // console.log(this.getAttribute("link_home"));
  }

  connectedCallback() {
    this.innerHTML = 
`
<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer All - START -->
<footer class="footer-signed-in-4-background-color">
  <div class="footer-signed-in-content">
    <p>Contact: Robert@Triviafy.com</p>
  </div>
</footer>
<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer All - END -->
`;
  }
}

customElements.define('footer-candidates-signed-in-component', FooterSignedInClassCandidates); 