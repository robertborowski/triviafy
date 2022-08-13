class FooterNotSignedInClassCandidates extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    // console.log(this.getAttribute("link_home"));
  }

  connectedCallback() {
    this.innerHTML = 
`
<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - footer all start -->
<footer class="footer-not-signed-in-candidates">
  <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - footer top start -->
  <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - footer top end -->
</footer>
<!-- - - - - - - - - - - - - - - - - - - - - - - - - - - footer all end -->
`;
  }
}

customElements.define('footer-candidates-not-signed-in-component', FooterNotSignedInClassCandidates);