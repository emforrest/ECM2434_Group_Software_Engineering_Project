## Base Template - `base.html`

Authored by Giulia Brown, `base.html` serves as the foundational template for the CO2 Saving Website, incorporating static and dynamic site content. It sets up basic structure including DOCTYPE, language, character encoding, responsive design, and includes the site title. External CSS for styling and boxicons for icons are linked. The navigation bar provides links to Register, Login, Leaderboard, User Profile, and Groups. A footer includes copyright information. External JavaScript libraries like jQuery, Popper.js, and Bootstrap are integrated for functionality. This template ensures a consistent look and facilitates easy navigation across the website.

## Choose Event Page - `chooseEvent.html`

Authored by Eleanor Forrest, `chooseEvent.html` is a webpage for admin users to select an event within the CarbonCommuter application. The page offers a navigation bar linking to Groups, Logout, User Leaderboard, and User Profile. Admins, identified as "gamemasters," are presented with a selection of events: Save X kg of CO2, Log X total journeys, Visit one location X times, and Visit every location at least once. A back button redirects to the admin homepage. Non-gamemaster users are informed the page is restricted. The footer reinforces site copyright. JavaScript enables redirection based on the selected event, enhancing user interaction.

## Confirm Event Page - `confirmEvent.html`

Created by Eleanor Forrest, `confirmEvent.html` facilitates event confirmation for admin users of the CarbonCommuter application. Featuring a consistent navigation bar with links to Groups, Logout, Leaderboard, and User Profile, it guides "gamemasters" through finalizing event details. Admins are prompted to fill out specific event parameters such as target amounts or selection from dropdowns, with fields dynamically generated based on event type. A JavaScript slider displays the value for range inputs, enhancing user interaction. The page includes a form submission for event creation with CSRF protection and an end date input. Non-gamemaster users are restricted from accessing this functionality. The footer maintains site-wide copyright consistency.

## Admin Home Page - `mainAdmin.html`

Authored by Abi Hinton and Eleanor Forrest, `mainAdmin.html` is the admin dashboard for the CarbonCommuter application. It features a standard navigation bar with links to Groups, Logout, Leaderboard, and User Profile, ensuring easy navigation. The page welcomes admins, specifically "gamemasters," with a greeting and the capability to create global events. A conditional display alerts admins if an event is already active, otherwise offering a "Create Event" button. A separate option to "Verify Journeys" is provided. Gamemaster restriction is enforced, with a script to redirect to the event creation page, ensuring controlled access. The footer maintains copyright information, emphasizing the professional and secure environment of the admin dashboard.

## Event Creation Success Page - `success.html`

Created by Eleanor Forrest, `success.html` confirms the successful addition of an event within the CarbonCommuter application. The page includes a consistent navigation bar, accommodating both authenticated and unauthenticated users with appropriate links such as Groups, Leaderboard, Logout, and Login. Specifically designed for "gamemasters," it displays a congratulatory message and the event's description, reinforcing the successful creation of a global event. A "Back to admin" button redirects gamemasters to the admin dashboard for further management. Restricted access is highlighted for non-gamemaster users. The footer underscores copyright, preserving the site's professional integrity.

## Journey Verification Page - `verify_journey.html`

`verify_journey.html` extends the base template to focus on the admin task of verifying suspicious journeys within the CarbonCommuter system. It maintains the consistent navigation bar from `base.html`, tailored for authenticated users, with links to Groups, Leaderboard, Logout, and User Profile. The main content presents a table where admins can review journeys flagged as suspicious. Each row displays a journey's details—user, date, time, reason for suspicion—and offers actions: approve or delete the journey, represented by checkmark and cross icons, respectively. A script enhances user interaction, making table rows clickable and redirecting to detailed journey information. This page is designed for admin use, streamlining the review process of flagged journeys to ensure data integrity.

## Group Page - `group_page.html`

`group_page.html` extends from the base layout to ensure site-wide consistency, specifically focusing on group details and interactions. The page dynamically titles itself with the group's name and adjusts the navigation bar based on user authentication. Main content highlights the group's name, membership status of the visitor, and different interaction options such as joining, leaving, or managing the group. For group leaders, additional controls are available for deleting the group or managing membership, including removal options for members and handling join requests. Links to member profiles provide a personal touch. The group's privacy settings dictate join options, distinguishing between open and request-to-join mechanisms. The footer reaffirms copyright, maintaining the site's professionalism.

## Search Groups Page - `search.html`

`search.html` sets its title to "Search Groups Page" and adapts the navigation bar according to user authentication status, offering links to Groups, Leaderboard, and Login/Logout. The page features a search bar for users to find groups by name. Below the search bar, search results are presented within individual cards that include the group's name and a "View Group" button, directing to the group's detailed page. If no groups match the search query, the page displays a "No groups found" message. The footer carries a copyright notice, emphasizing the ownership and rights of the website content.

## User Groups Home Page - `user_groups_home_page.html`

The User Groups Home Page is designed for users to manage their group memberships and explore new groups. The page title is set to "User Groups Home Page," and the navigation bar includes user-centric links. Main content is split into sections for current group memberships and group discovery:

- **Your Groups**: Displays cards for each group the user belongs to, with options to view each group. If the user isn't in any groups, a message indicates this.
- **Search for Groups**: Offers a direct link to the search groups page, encouraging users to find and join new groups.
- **Create a New Group**: Provides a form for users to create a new group, with fields for the group name and privacy settings.

This page serves as a central hub for users to engage with the community, whether by maintaining existing connections or forging new ones.

## Leaderboard - `leaderboard.html`

Authored by Jack Skinner, the `leaderboard.html` page presents a comprehensive view of user and group achievements in CO2 savings. It features a main leaderboard showcasing individual users, a weekly leaderboard for timely accomplishments, and a group leaderboard to highlight collective efforts. Each section uses symbols (🥇, 🥈, 🥉) to denote the top three positions, adding a competitive edge. The design ensures easy navigation between different leaderboard categories, making it straightforward for users to compare rankings. This page plays a key role in fostering a sense of community and competition, motivating further participation in carbon-saving activities.

## User Leaderboard - `user_leaderboard.html`

Authored by Jack Skinner, `user_leaderboard.html` showcases various leaderboards to highlight achievements within the CarbonCommuter community, specifically catering to logged-in users. This page features multiple sections:

- **Leaderboard**: A table displaying all users ranked by their CO2 savings, with special icons (🥇, 🥈, 🥉) for the top three performers. Users' names are clickable, linking to their profiles.
- **Weekly Leaderboard**: Focuses on weekly achievements, encouraging short-term engagement and competition. It also uses medals to denote top performers and links to user profiles.
- **Group Leaderboard**: Highlights groups leading in CO2 savings, fostering a sense of community and collective effort. Group names link to their respective pages.
- **Follower Leaderboard**: A unique addition showcasing the achievements of users followed by the logged-in user, adding a personal touch to the competition.

Each section is designed to motivate users through recognition, fostering a competitive yet community-oriented environment.

## Login Page - `login.html`

Created by Jack Skinner, Giulia Brown, and Abi Hinton, `login.html` serves as the entry point for users to access their accounts on the platform, mistakenly titled "Registration page" which should be "Login Page". The layout integrates a minimalist navigation bar directing authenticated users to groups and leaderboard sections. It features a straightforward login form prompting for username and password, with an error message display for input validation. For new visitors, a registration link invites them to create an account. Logged-in users receive a prompt about their status with an option to logout, enhancing user experience by addressing session management directly. The footer reinforces the site's copyright.

## Logout Page - `logout.html`

Developed by Jack Skinner, Giulia Brown, and Abi Hinton, the logout page offers a straightforward mechanism for users to securely exit their accounts. Titled "Logout page," it streamlines the navigation bar to essential links like the leaderboard and user profile. Central to the page is a confirmation prompt ensuring users intentionally choose to logout, addressed through a submission form guarded by CSRF tokens for security. For visitors not logged in, it thoughtfully provides a prompt to login or an invitation to register, accommodating all user states. This design prioritizes user intention and security, facilitating a clear and concise logout process. The consistent footer across the site underlines copyright.

## Main Home Page - `main.html`

Authored by Jack Skinner and Giulia Brown, `main.html` introduces users to the CarbonCommuter platform. Titled "CO2 Saving Website," it simplifies the navigation bar with essential links: Register, Login, and Leaderboard. The core of the page is a welcoming message encouraging new visitors to register and start tracking their carbon emissions, offering a community-focused experience through groups and competitive leaderboards. It provides straightforward access with buttons for registration, login, and leaderboard viewing, each followed by a brief directive. This layout aims to onboard new users while re-engaging returning visitors. The footer across the site underscores the copyright, ensuring brand consistency.

## Admin Home Page - `mainAdmin.html`

The `mainAdmin.html` page is specifically designed for administrators of the CO2 Saving Website, extending from the `base.html` template with a focus on admin responsibilities. The page features a navigation bar with links to Register, Login, Leaderboard, User Profile, and Groups, emphasizing the admin's unique role in the community. It highlights the importance of admin tasks such as managing groups and ensuring the validity of carbon emission inputs. The welcome message underscores the admin's crucial role in overseeing the platform's impact on carbon savings, inviting them to actively participate in the community's efforts to reduce emissions.

## Privacy Policy - `PrivacyPolicy.html`

Created by Jack Skinner, `PrivacyPolicy.html` presents the Privacy Policy of the CarbonCommuter platform, accessible through a simplified navigation bar tailored for both authenticated and unauthenticated users. The document, last updated on 17/03/2024, details the collection, use, and disclosure of personal data by the Carbon Commuter mobile app. It highlights the types of data collected, including location and personal data, and the purposes behind this collection—to enhance service provision. The policy outlines data usage practices, emphasizing the commitment to data security and the conditions under which data is stored or shared. Notably, it assures users of the protective measures against data breaches and unauthorized access. The document also mentions the protocol for policy updates and encourages users to periodically review the changes. A contact email provides a direct line for privacy concerns, reaffirming user rights and the app's dedication to privacy adherence. The footer echoes the site-wide copyright notice, reinforcing the platform's professional integrity.

## Register Page - `register.html`

Created by Jack Skinner, Giulia Brown, and Abi Hinton, the registration page facilitates new user sign-ups for the CO2 Saving Website, ensuring accessibility through a clearly structured form. The page, titled "Register - CO2 Saving Website," provides a simplified navigation bar suited for both new and returning users with direct links to login and leaderboard. It features a comprehensive form collecting essential details such as first name, surname, username, email, and password with a secondary password input for confirmation. Additionally, it includes a mandatory acceptance checkbox for the Privacy Policy, reinforcing the site's commitment to data protection. An error display mechanism alerts users to any input discrepancies. For those already registered, a prompt redirects them to the login page. The footer maintains copyright consistency across the site.

## Base Template - `base.html`

Authored by Giulia Brown, `base.html` establishes the foundational HTML structure for all pages within the CarbonCommuter website. It sets universal HTML, head, and body tags, incorporating responsive meta tags and importing essential styles and scripts for consistent design and functionality across the site. The stylesheet links include CarbonCommuter's custom CSS, Boxicons for icons, and Bootstrap for responsive layout components. JavaScript sources for dynamic content and Bootstrap's components enhance interactivity.

The template defines several overrideable Django template blocks (`script`, `body`, `navbar`, `content`) allowing derived pages to inject specific content or scripts while maintaining a consistent navigation bar and site-wide header. Notably, the navbar dynamically adjusts to include an 'Admin' link for users identified as 'gamemasters', ensuring easy access to administrative functions. This base structure is pivotal for ensuring a cohesive user experience across the CarbonCommuter platform.

## Cancel Journey Page - `cancel.html`

`cancel.html` integrates with the `base.html` template to provide a focused interface for users contemplating the cancellation of an active journey on the CarbonCommuter platform. The page is succinctly titled "Delete Journey" and retains a streamlined navigation bar leading to the Leaderboard and User Profile, emphasizing essential user actions. Central to the page is a confirmation prompt that stresses the irreversibility of cancelling a journey, aiming to ensure users make an informed decision. It features a form facilitating the cancellation process, alongside a "Go Back" button for reconsideration, balancing user autonomy with caution. This setup underscores the platform's commitment to user control over their data, within a structure that consistently echoes the site's branding and copyright through the footer.

## Delete Journey Page - `delete.html`

`delete.html` works within the `base.html` framework, specifically enabling users to permanently remove a journey on the CarbonCommuter platform. Titled "Delete Journey," it features a navigation bar for easy access to the Leaderboard and User Profile, streamlining navigation. The centerpiece is a confirmation form that underscores the permanence of the deletion process, aiming to prompt thoughtful user action. Buttons offer a choice between cancelling the action and proceeding with the deletion, balancing user autonomy against irreversible decisions. This design marries simplicity with caution, all under the consistent branding and copyright assurance of the site-wide footer.

## End Journey Page - `end_journey.html`

The page, titled "End Your Journey," provides a straightforward and engaging interface for users to confirm their current location as the endpoint of their journey. It includes a dynamic map display, leveraging Google Maps API for precise geolocation, and offers users the choice to manually input their location if automatic detection fails. Key features include animated visuals to engage users while their location is being fetched and alternative options for location input. A significant option presented is the ability to cancel the current journey.

## Journey Completion Page - `finished.html`

`finished.html` extends the `base.html` template to celebrate the user's achievement in completing a journey. The page,"Success," offers a navigation bar for both logged-in and guest users, providing essential links like Groups, Leaderboard, and Login/Logout. It congratulates users, showcasing the distance travelled, time taken, mode of transport, and the amount of CO2 saved. Two buttons offer users the options to view detailed journey information or return to the homepage, supported by straightforward JavaScript for navigation.

## Start A Journey Page - `start_journey.html`

`start_journey.html, introduces a platform for users to initiate their journeys on CarbonCommuter. Titled "Start A Journey," the page allows navigation and utilises the Google Maps API for accurate location services. Users can either automatically obtain their starting location or input it manually, ensuring flexibility in how journeys begin. The page progresses through stages: obtaining location, confirming it, and selecting the mode of transport, each facilitated by intuitive buttons and dropdown menus. Additional instructions or errors are handled gracefully.
## Journey Started Page - `started.html`

`started.html` extends from `base.html` to show the start of a new journey by the user. The page, aptly titled "Success," features a navigation bar tailored for both logged-in and guest users, providing links to Groups, Leaderboard, Login/Logout, and User Profile. It congratulates users on beginning their "new adventure" and emphasises the environmental impact of their journey. Users are reminded to end their journey on the website to contribute to leaderboard rankings. A "Go home" button offers a return to the user dashboard.

## Account Deletion Confirmation Page - `confirm.html`

`confirm.html` is an interface designed within the `base.html` framework for users considering the irreversible action of deleting their CarbonCommuter account The cancellation option links back to settings, allowing users to not delete their account.
## User Home Page - `home.html`

`home.html` serves as the personalised dashboard for users of the CO2 Saving Website, extending from the `base.html` template. The page title "CO2 Saving Website" heads a navigation bar for user interaction, including links to Groups, Leaderboard, My Journeys, and Logout/Login. It also contains user-specific details like streaks, name, email, username, join date, and provides options to edit the profile or view the public profile. It also displays ongoing global challenges, total CO2 savings, and user badges for streaks, locations visited, and leaderboard achievements. Following lists and badges visually represent user achievements and community involvement.
## Journey Detail Page - `journey.html`

`journey.html` extends the `base.html` template. The"Success" page, offers navigation options relevant to both users and guests. It presents the journey's specifics, such as distance travelled, time taken, CO2 savings, and the mode of transport used. Additional details include start and end times, along with addresses for journeys with location data. For journeys lacking this data, a note clearly states the absence of location information. Two actionable buttons, "Go back" and "Delete Journey," give users control over their navigation and management of journey records. This setup ensures users can easily access, review, and manage their journey details.

## User Journeys Page - `journeys.html`

`Journeys.html` provides a view of a user's journeys on the CarbonCommuter platform, extending the `base.html`. It features a navigation bar for easy access to groups, leaderboard, and logout/login functionalities, for both authenticated and guest users.
The main content showcases a table listing the user's journeys, displaying journey number, date, distance traveled, CO2 savings, transport mode, and actions - specifically, an option to delete each journey. An empty state message informs users when no journeys have been recorded, and JavaScript functionality enhances the table's interactivity, making each row clickable for detailed journey views.

## Public User Profile Page - `profile.html`

`profile.html` creates a public-facing profile for users of the CarbonCommuter platform, integrated with the `base.html` template for consistent navigation. The "Profile," enables users to showcase their environmental contributions and connect with the community. It displays the user's username, total carbon savings, join date, and earned and unlearned badges. Depending on the viewer's relationship to the profile, the page adapts to show either a "Back" button for personal profiles or a "Follow/Unfollow" button for others.
## User Settings Page - `settings.html`

`settings.html` allows CarbonCommuter users to alter their settings within the application, building on the `base.html` template. The page, titled "Settings," provides a navigation bar suited for both logged in and guest users, allowing easy site navigation. Its features allow users to update their first name, last name, username, and email, with a requisite password entry for changes to take effect, emphasising security. Also a distinct section for account deletion making sure the users understand the irreversible nature of this action.
