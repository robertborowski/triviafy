class FooterNotSignedInClassCandidates extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    // console.log(this.getAttribute("link_home"));
  }

  connectedCallback() {
    this.innerHTML = `
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer All - START -->
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer All - END -->
    `;
  }
}

customElements.define('footer-candidates-not-signed-in-component', FooterNotSignedInClassCandidates);