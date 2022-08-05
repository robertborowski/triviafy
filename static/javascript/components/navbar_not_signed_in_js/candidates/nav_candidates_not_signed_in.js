class NavbarCandidatesNotSignedInClass extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    console.log(this.getAttribute("slack_state_uuid_js"));
  }

  connectedCallback() {
    this.innerHTML = `
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - navbar start - - - - - - - - - - - - - - - - - - - - - - - - - - -->
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - navbar end - - - - - - - - - - - - - - - - - - - - - - - - - - -->
    `;
  }
}

customElements.define('nav-candidates-not-signed-in-component', NavbarCandidatesNotSignedInClass);