class NewUserOnboardingStepsClass extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    // console.log(this.getAttribute("link_home"));
  }

  connectedCallback() {
    this.innerHTML = `
    <div class="client-company-and-channel-names">
      <span>${this.getAttribute("new_user_onboarding_steps_from_html")}</span>
    </div>
    `;
  }
}

customElements.define('new-user-onboarding-steps-component', NewUserOnboardingStepsClass);