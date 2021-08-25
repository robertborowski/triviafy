class NavbarNotSignedInClass extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    console.log(this.getAttribute("slack_state_uuid_js"));
  }

  connectedCallback() {
    this.innerHTML = `
    <nav class="navbar-not-signed-in box-shadow-sm-grey box-shadow-rounded">
  
      <!-- Logo and Company Name -->
      <div class="company-name-and-logo-navbar-not-signed-in">
        <!-- Logo -->
        <a href="${this.getAttribute("link_home_js")}"><img src="/static/images/logo/Logo.png" class="company-logo-navbar-not-signed-in" alt="Triviafy icon/logo"></a>
        <!-- Company Name -->
        <h1 class="company-name-navbar-not-signed-in"><a href="${this.getAttribute("link_home_js")}">Triviafy</a></h1>
      </div>
    
      <a href="#" class="toggle-button-not-signed-in">
        <span class="bar top-bar"></span>
        <span class="bar middle-bar"></span>
        <span class="bar bottom-bar"></span>
      </a>
    
      <!-- Navbar links -->
      <div class="navbar-links-not-signed-in">
        <ul>
          <li><a href="${this.getAttribute("link_about_js")}">About</a></li>
          
          <li><a href="https://slack.com/openid/connect/authorize?response_type=code&scope=openid%20profile%20email&client_id=2010284559270.2041074682000&state=${this.getAttribute("slack_state_uuid_js")}&redirect_uri=https://triviafy.com/slack/oauth_redirect"><img alt="Sign in with Slack" height="40" width="170" src="https://platform.slack-edge.com/img/sign_in_with_slack.png" srcSet="https://platform.slack-edge.com/img/sign_in_with_slack.png 1x, https://platform.slack-edge.com/img/sign_in_with_slack@2x.png 2x" class="slack-image-button-li" /></a></li>

          <li><a href="https://slack.com/oauth/v2/authorize?client_id=2010284559270.2041074682000&scope=incoming-webhook,team:read,users.profile:read,users:read,users:read.email&state=${this.getAttribute("slack_state_uuid_js")}&user_scope=openid,profile,email"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" class="slack-image-button-li" /></a></li>
        </ul>
      </div>
    </nav>
    <div class="spacer-navbar-not-signed-in"></div>
    `;
  }
}

customElements.define('nav-not-signed-in-component', NavbarNotSignedInClass);