class NavbarNotSignedInClass2 extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    console.log(this.getAttribute("slack_state_uuid_js"));
  }

  connectedCallback() {
    this.innerHTML = `
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Top Shadow START -->
    <div class="navbar-2-outline-shadow default-box-shadow-grey-reg">
      <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Top Shadow END -->
      
      <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Entire START -->
      <nav class="navbar-2-not-signed-in">
        
        <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Logo and Name START -->
        <div class="navbar-2-logo-and-name-section">
          <a href="${this.getAttribute("link_home_js")}"><img src="/static/images/employee_engagement/logo/Logo.png" alt="Triviafy Logo" class="navbar-2-not-signed-in-logo"></a>
          <div class="brand-title-2-not-signed-in"><a href="${this.getAttribute("link_home_js")}">Triviafy</a></div>
        </div>
        <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Logo and Name END -->


        <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Hamburger Toggle START -->
        <a href="#" class="toggle-button-2">
          <span class="toggle-bar-2"></span>
          <span class="toggle-bar-2"></span>
          <span class="toggle-bar-2"></span>
        </a>
        <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Hamburger Toggle END -->


        <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 1 - START -->
        <div class="navbar-links-2-not-signed-in">
          <ul>
            <li class="navbar-list-item-1"><a href="#">How It Works <i class="fas fa-angle-down navbar-drop-down-arrow-1"></i></a>
              <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - START -->
              <ul class="links-level-2 default-box-shadow-grey-reg">
                <li><a href="${this.getAttribute("pdf_slack_setup_js")}"><i class="fas fa-tools font-awesome-icon"></i>Slack Setup</a></li>
                <li><a href="${this.getAttribute("pdf_example_quiz_js")}"><i class="fas fa-calendar-week font-awesome-icon"></i>Analytics Example Quiz</a></li>
                <li><a href="${this.getAttribute("pdf_example_quiz_javascript_js")}"><i class="fab fa-js-square font-awesome-icon"></i>JavaScript Example Quiz</a></li>
                <li><a href="${this.getAttribute("pdf_example_quiz_excel_js")}"><i class="fas fa-file-excel font-awesome-icon"></i>Excel Example Quiz</a></li>
                <li><a href="${this.getAttribute("pdf_example_quiz_sql_js")}"><i class="fas fa-database font-awesome-icon"></i>SQL Example Quiz</a></li>
                <li><a href="${this.getAttribute("pdf_example_quiz_tableau_js")}"><i class="fas fa-chart-pie font-awesome-icon"></i>Tableau Example Quiz</a></li>
                <li><a href="${this.getAttribute("pdf_example_quiz_mixed_categories_js")}"><i class="fas fa-pencil-ruler font-awesome-icon"></i>Custom Quiz</a></li>
              </ul>
              <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - END -->
            </li>
            <li class="navbar-list-item-2"><a href="#">Resources <i class="fas fa-angle-down navbar-drop-down-arrow-2"></i></a>
              <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - START -->
              <ul class="links-level-2 default-box-shadow-grey-reg">
                <li><a href="${this.getAttribute("link_faq_js")}"><i class="fas fa-question-circle font-awesome-icon"></i>FAQ</a></li>
                <li><a href="${this.getAttribute("link_about_js")}"><i class="fas fa-puzzle-piece font-awesome-icon"></i>About</a></li>
                <li><a href="${this.getAttribute("link_privacy_js")}"><i class="fas fa-lock font-awesome-icon"></i>Privacy</a></li>
                <li><a href="${this.getAttribute("link_blog_js")}"><i class="fas fa-pen-square font-awesome-icon"></i>Blog</a></li>
              </ul>
              <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - END -->
            </li>
            <li class="navbar-list-item-3"><a href="#">Login <i class="fas fa-angle-down navbar-drop-down-arrow-3"></i></a>
              <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - START -->
              <ul class="links-level-2 default-box-shadow-grey-reg">
                <li><a href="https://slack.com/openid/connect/authorize?response_type=code&scope=openid%20profile%20email&client_id=2010284559270.2041074682000&state=${this.getAttribute("slack_state_uuid_js")}&redirect_uri=https://triviafy.com/slack/oauth_redirect"><i class="fab fa-slack font-awesome-icon"></i>Sign in with Slack</a></li>
                <!-- <li><a href="https://slack.com/openid/connect/authorize?response_type=code&scope=openid%20profile%20email&client_id=2010284559270.2041074682000&state=${this.getAttribute("slack_state_uuid_js")}&redirect_uri=https://triviafy.com/slack/oauth_redirect"><img alt="Sign in with Slack" height="40" width="170" src="https://platform.slack-edge.com/img/sign_in_with_slack.png" srcSet="https://platform.slack-edge.com/img/sign_in_with_slack.png 1x, https://platform.slack-edge.com/img/sign_in_with_slack@2x.png 2x" class="slack-image-button-li" /></a></li> -->

                <li><a class="typeform-share button" href="https://form.typeform.com/to/NPVjDw88?typeform-medium=embed-snippet" data-mode="popup" data-size="100" target="_blank"><i class="fab fa-windows font-awesome-icon"></i>Microsoft Teams</a></li>
                <script> (function() { var qs,js,q,s,d=document, gi=d.getElementById, ce=d.createElement, gt=d.getElementsByTagName, id="typef_orm_share", b="https://embed.typeform.com/"; if(!gi.call(d,id)){ js=ce.call(d,"script"); js.id=id; js.src=b+"embed.js"; q=gt.call(d,"script")[0]; q.parentNode.insertBefore(js,q) } })() </script>
                
                <li><a class="typeform-share button" href="https://form.typeform.com/to/NPVjDw88?typeform-medium=embed-snippet" data-mode="popup" data-size="100" target="_blank"><i class="far fa-envelope font-awesome-icon"></i>Email</a></li>
                <script> (function() { var qs,js,q,s,d=document, gi=d.getElementById, ce=d.createElement, gt=d.getElementsByTagName, id="typef_orm_share", b="https://embed.typeform.com/"; if(!gi.call(d,id)){ js=ce.call(d,"script"); js.id=id; js.src=b+"embed.js"; q=gt.call(d,"script")[0]; q.parentNode.insertBefore(js,q) } })() </script>
              </ul>
              <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - END -->
            </li>
            <li class="navbar-list-item-4"><a href="#">Create Account <i class="fas fa-angle-down navbar-drop-down-arrow-4"></i></a>
              <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - START -->
              <ul class="links-level-2 default-box-shadow-grey-reg">
                
                <li><a href="https://slack.com/oauth/v2/authorize?client_id=2010284559270.2041074682000&scope=incoming-webhook,team:read,users.profile:read,users:read,users:read.email&state=${this.getAttribute("slack_state_uuid_js")}&user_scope=openid,profile,email"><i class="fab fa-slack font-awesome-icon"></i>Add to Slack</a></li>
                <!-- <li><a href="https://slack.com/oauth/v2/authorize?client_id=2010284559270.2041074682000&scope=incoming-webhook,team:read,users.profile:read,users:read,users:read.email&state=${this.getAttribute("slack_state_uuid_js")}&user_scope=openid,profile,email"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" class="slack-image-button-li" /></a></li> -->

                <li><a class="typeform-share button" href="https://form.typeform.com/to/NPVjDw88?typeform-medium=embed-snippet" data-mode="popup" data-size="100" target="_blank"><i class="fab fa-windows font-awesome-icon"></i>Microsoft Teams</a></li>
                <script> (function() { var qs,js,q,s,d=document, gi=d.getElementById, ce=d.createElement, gt=d.getElementsByTagName, id="typef_orm_share", b="https://embed.typeform.com/"; if(!gi.call(d,id)){ js=ce.call(d,"script"); js.id=id; js.src=b+"embed.js"; q=gt.call(d,"script")[0]; q.parentNode.insertBefore(js,q) } })() </script>

                <li><a class="typeform-share button" href="https://form.typeform.com/to/NPVjDw88?typeform-medium=embed-snippet" data-mode="popup" data-size="100" target="_blank"><i class="far fa-envelope font-awesome-icon"></i>Email</a></li>
                <script> (function() { var qs,js,q,s,d=document, gi=d.getElementById, ce=d.createElement, gt=d.getElementsByTagName, id="typef_orm_share", b="https://embed.typeform.com/"; if(!gi.call(d,id)){ js=ce.call(d,"script"); js.id=id; js.src=b+"embed.js"; q=gt.call(d,"script")[0]; q.parentNode.insertBefore(js,q) } })() </script>
              </ul>
              <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 2 - END -->
            </li>
            <div class="navbar-not-signed-in-demo-button-section">
              <a href="${this.getAttribute("link_demo_js")}"><button class="default-button-format default-button-format-primary-color navbar-not-signed-in-button-position">Request a demo</button></a>
            </div>
          </ul>
        </div>
        <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Links - Level 1 - END -->
        
      </nav>

    </div>
    <div class="spacer-navbar-not-signed-in-2"></div>
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Navbar - Entire END -->
    `;
  }
}

customElements.define('nav-not-signed-in-component-2', NavbarNotSignedInClass2);