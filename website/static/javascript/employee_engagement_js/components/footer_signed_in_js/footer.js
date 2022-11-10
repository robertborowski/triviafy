class FooterSignedInClass extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    // console.log(this.getAttribute("link_home"));
  }

  connectedCallback() {
    this.innerHTML = `
    <footer class="logged-in-footer-tag">
      <p>Contact: support@triviafy.com | All Rights Reserved. 2022 Triviafy</p>
    </footer>
    `;
  }
}

customElements.define('footer-signed-in-component', FooterSignedInClass);