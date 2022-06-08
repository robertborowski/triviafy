class CompanyNameChannelClass extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    // console.log(this.getAttribute("link_home"));
  }

  connectedCallback() {
    this.innerHTML = `
    <div class="client-company-and-channel-names">
      <span>${this.getAttribute("company_name_js")}</span>
      <span>${this.getAttribute("channel_name_js")}</span>
      <span>${this.getAttribute("free_trial_ends_info_js")}</span>
    </div>
    `;
  }
}

customElements.define('company-name-channel-component', CompanyNameChannelClass);