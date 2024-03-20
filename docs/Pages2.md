## Base Template - `base.html`

This serves as the template for the Website. It sets up basic structures. External CSS and boxicons are also linked. The navbar provides links to Register, Login, Leaderboard, User Profile, and Groups. A footer includes copyright information. External JavaScript libraries are integrated. This template ensures a consistent look and facilitates easy navigation across the website.

## Choose Event Page - `/admin/chooseEvent`

The choose event page allows users who are authorised as gamemasters to select one of the following global events: Save X kg of CO2, Log X total journeys, Visit one location X times, and Visit every location at least once. Non gamemasters cannot access this page.

## Confirm Event Page - `/admin/confirmEvent`

This page simply allows gamemasters to view the events that they have created, and confirm the details before deployng the event for the whole website. Access is restricted for non gamemasters. Once the event has been confirmed, a success message will appear. S

## Admin Home Page - `/admin`

The admin home page is acessible to users that have the 'Gamemaster' Tag. This tag is assigned in the database and allows users to create events for all users in the app and manually review all journeys that our system has flagged as being suspicious. If a user who is not an admin tries to acess this page they will not be able to access anything and will instaid get a messgae that they do not have permissions. 

## Journey Verification Page - `/admin/verify`

This page is used to display all journeys that our automatic system has flagged as being suspicious - By how much quicker the journey has occured compared to the apis estimate for how long it should take, or a journey is too long. These can be reviewed, and approved if the gamemaster thinks that the journey made is valid, and denied if the journey was clearly fake. This incresases the integrity of our website by ensuring we have a way to moderate journeys so positions on the leaderboard are earned, and cant be cheated. 

## Group Page - `/groups/view/<group_id>`
This page displays the public information about a group. The group leader and group members. It also allows you to join the group, which will then be sent to the group leader for manual review. 

## Search Groups Page - `/groups/search`

The search group page allows user to put in a group name. Underneath in Search Results a list of groups with similar names appear, with the group name and a button to view the group. The button then redirects you to that gruops home page. 

## User Groups Home Page - `/groups`

The User Groups Home Page is designed for users to manage their group memberships and explore new groups. The page title is set to "User Groups Home Page," and the navigation bar includes user-centric links. Main content is split into sections for current group memberships and group discovery:

- **Your Groups**: Displays cards for each group the user belongs to, with options to view each group. If the user isn't in any groups, a message indicates this.
- **Search for Groups**: Offers a direct link to the search groups page, encouraging users to find and join new groups.
- **Create a New Group**: Provides a form for users to create a new group, with fields for the group name and privacy settings.

This page serves as a central hub for users to engage with the community, whether by maintaining existing connections or forging new ones.

## Leaderboard - `./leaderboard`

The leaderboard page allows anyone without an account to view the status of the leaderbaord. It will display the all time carbon savings for the top 10 users on the system. You can also see the top users this week, and the top groups on the website. 

## Leaderboard `./leaderboard/user_leaderboard`

The user_leaderboard page allows users who are logged in to view additional information on top of the standard leaderboard. You can click on users and groups on the leaderboard to view their public information, You can see how you are doing in comparision to people you are following. The users at the top of the weekly leaderboard at the end of the week will be awarded with a badge. 

## Login - `./login`

Login follows a standard website login template, with a form that contains fields for the username and password, and a submit button. On submit, the login details should be verified against the database using the built-in Django authentication system. If successfull, the user is redirected to the [User Home](#user-home---user) page, otherwise an error is displayed and they must try again. If this page is visited by an autenticated user, it should instead warn them and give them the option to logout.

## Logout - `./login/logout`

For the Logout page, if the user is authenticated, it should ask for a confirmation if they want to logout, then logout the user if they click the button. If they're not authenticated, it should offer a link to the login/register pages instead.


## Home - `./`

The Home page contains information about the application, and is the first page to be visited when users discover the site. It should encourage users to register for an account or login if they already have one, as well as highlight the advantages of using the system, such as linking the Leaderboard. This page should only be accessible to un-authenticated users, any users already logged in should be redirected to the [User Home](#user-home---user) page.

## Privacy Policy `./register/PrivacyPolicy`
CarbonCommuter handles sensitive location data, and the privacy policy outlines how the app uses your personal data. We outline how sensitive location data is deleted after 2 weeks, and that this data is secure and encrypted and stored in a secure database (oracle)

## Register - `./register`

Register follows a standard website register template, with a form that contains fields for the first and last name, username, email address, password, and another to re-enter the password, as well as a prompt to a privacy policy that they must accept. The password is checked against standard security checks (such as length and whether it is a common password), then verified to match the re-entered password. If these checks pass then a new user is created within the database. The user is then redirected to the user home page.

## Base Template - `base.html`

The base template is the foundation for the rest of the website. Each page is built upon this file. The file contains some standard CSS files, JS scripts for mobile compatibility, The navbar which can then be built upon to show appropriate infromation for each page. It has a block for users to then add the body.

## Cancel Journey Page - `cancel.html`

`cancel.html` integrates with the `base.html` template to provide a focused interface for users contemplating the cancellation of an active journey on the CarbonCommuter platform. The page is succinctly titled "Delete Journey" and retains a streamlined navigation bar leading to the Leaderboard and User Profile, emphasizing essential user actions. Central to the page is a confirmation prompt that stresses the irreversibility of cancelling a journey, aiming to ensure users make an informed decision. It features a form facilitating the cancellation process, alongside a "Go Back" button for reconsideration, balancing user autonomy with caution. This setup underscores the platform's commitment to user control over their data, within a structure that consistently echoes the site's branding and copyright through the footer.

## Delete Journey Page - `.user/`

`delete.html` works within the `base.html` framework, specifically enabling users to permanently remove a journey on the CarbonCommuter platform. Titled "Delete Journey," it features a navigation bar for easy access to the Leaderboard and User Profile, streamlining navigation. The centerpiece is a confirmation form that underscores the permanence of the deletion process, aiming to prompt thoughtful user action. Buttons offer a choice between cancelling the action and proceeding with the deletion, balancing user autonomy against irreversible decisions. This design marries simplicity with caution, all under the consistent branding and copyright assurance of the site-wide footer.

## End Journey Page - `end_journey.html`

`end_journey.html`, crafted by Eleanor Forrest, Jack Skinner, Giulia Brown, and Sam Townley, facilitates the completion of a user's journey on the CarbonCommuter platform. The page, titled "End Your Journey," provides a straightforward and engaging interface for users to confirm their current location as the endpoint of their journey. It includes a dynamic map display, leveraging Google Maps API for precise geolocation, and offers users the choice to manually input their location if automatic detection fails.

Key features include animated visuals to engage users while their location is being fetched and alternative options for location input, enhancing user experience. A significant option presented is the ability to cancel the current journey, emphasizing user control and flexibility in journey management. This page stands out for its blend of interactive elements, user-friendly design, and essential functionalities, all encapsulated within a structure that maintains site-wide consistency, including a navigation bar and footer.

## Journey Completion Page - `finished.html`

`finished.html` extends the `base.html` template to celebrate the user's achievement in completing a journey on the CarbonCommuter platform. The page, aptly titled "Success," offers a navigation bar tailored for both logged-in and guest users, providing essential links like Groups, Leaderboard, and Login/Logout. It warmly congratulates users, showcasing the distance traveled, time taken, mode of transport, and the amount of CO2 saved in an engaging and informative manner. Two buttons offer users the options to view detailed journey information or return to the homepage, supported by straightforward JavaScript for navigation. This celebratory page not only acknowledges the user's effort towards reducing carbon emissions but also encourages further engagement with the platform through its content and layout, all while maintaining the site's consistent branding in the footer.

## Start A Journey Page - `start_journey.html`

`start_journey.html`, created by Eleanor Forrest, Jack Skinner, Giulia Brown, and Sam Townley, introduces a comprehensive platform for users to initiate their journeys on CarbonCommuter. Titled "Start A Journey," the page is equipped with a dynamic navigation bar and utilizes the Google Maps API for accurate location services. Users can either automatically obtain their starting location or input it manually, ensuring flexibility in how journeys begin. The page progresses through stages: obtaining location, confirming it, and selecting the mode of transport, each facilitated by intuitive buttons and dropdown menus. Additional instructions or errors are handled gracefully, maintaining user engagement. This interactive setup encourages active participation in sustainable commuting, reflected in the detailed design and thoughtful implementation of user interactions, all within a consistent site-wide aesthetic.

## Journey Started Page - `started.html`

`started.html` extends from `base.html` to celebrate the initiation of a new journey by the user, reinforcing the CarbonCommuter's commitment to reducing CO2 emissions. The page, aptly titled "Success," features a navigation bar tailored for both logged-in and guest users, providing links to Groups, Leaderboard, Login/Logout, and User Profile. It warmly congratulates users on beginning their "new adventure" and emphasizes the environmental impact of their journey, quantifying the CO2 savings to motivate and educate. Users are reminded to end their journey on the website to contribute to leaderboard rankings. A "Go home" button offers a seamless return to the user dashboard, encapsulated within a design that prioritizes user encouragement and engagement, all while aligning with the site's copyright in the footer.

## Account Deletion Confirmation Page - `confirm.html`

`confirm.html` is a focused interface designed within the `base.html` framework for users considering the irreversible action of deleting their CarbonCommuter account. The page presents a solemn confirmation prompt, directly addressing the gravity of account deletion and its permanent consequences. A form facilitates the action, offering a "Delete my account" button that starkly contrasts the cancellation option, emphasizing the finality of the decision. The cancellation option links back to settings, allowing users an escape route if they're hesitant or change their mind. This design prioritizes clear communication and user consent, ensuring users are fully aware of the implications of their choice.

## User Home Page - `home.html`

Authored by Giulia Brown and Eleanor Forrest, `home.html` serves as the personalized dashboard for users of the CO2 Saving Website, extending from the `base.html` template. The page title "CO2 Saving Website" heads a navigation bar tailored for user interaction, including links to Groups, Leaderboard, My Journeys, and Logout/Login. It showcases user-specific details like streaks, name, email, username, join date, and provides options to edit the profile or view the public profile. Additionally, it displays ongoing global challenges, total CO2 savings, and user badges for streaks, locations visited, and leaderboard achievements. Interactive elements, like starting, ending, or canceling a journey, enhance user engagement. Following lists and badges visually represent user achievements and community involvement, all wrapped in a design that echoes the site's commitment to environmental impact through personal action.

## Journey Detail Page - `journey.html`

`journey.html` extends the `base.html` template to provide a detailed overview of a specific journey on the CarbonCommuter platform. This page, marked by a "Success" title, offers navigation options relevant to both authenticated and guest users. It presents the journey's specifics, such as distance traveled, time taken, CO2 savings, and the mode of transport used. Additional details include start and end times, along with addresses for journeys with location data. For journeys lacking this data, a note clearly states the absence of location information. Two actionable buttons, "Go back" and "Delete Journey," give users control over their navigation and management of journey records. This setup ensures users can easily access, review, and manage their journey details within a user-centric design framework, all while aligning with the site-wide commitment to environmental impact tracking and user engagement.

## User Journeys Page - `journeys.html`

Created by Eleanor Forrest, `journeys.html` provides a comprehensive view of a user's journeys on the CarbonCommuter platform, extending the `base.html` template for consistent site navigation and style. The page, titled "Leaderboard," mistakenly, should likely be titled "Your Journeys" or similar, to accurately reflect its content. It features a navigation bar for easy access to groups, leaderboard, and logout/login functionalities, catering to both authenticated and guest users.

The main content showcases a table listing the user's journeys, displaying journey number, date, distance traveled, CO2 savings, transport mode, and actions - specifically, an option to delete each journey. This setup not only offers detailed insights into personal environmental contributions but also allows for direct management of journey records. An empty state message informs users when no journeys have been recorded, and JavaScript functionality enhances the table's interactivity, making each row clickable for detailed journey views. This page effectively merges user engagement with actionable insights into their commuting habits.

## Public User Profile Page - `profile.html`

Authored by Eleanor Forrest, `profile.html` crafts a public-facing profile for users of the CarbonCommuter platform, seamlessly integrating with the `base.html` template for consistent navigation. This page, aptly titled "Profile," enables users to showcase their environmental contributions and connect with the community. It displays the user's username, total carbon savings, join date, and earned badges, offering a glimpse into their achievements and commitment to reducing CO2 emissions. Depending on the viewer's relationship to the profile, the page adapts to show either a "Back" button for personal profiles or a "Follow/Unfollow" button for others, fostering community engagement and interaction. This adaptability enhances the user experience by providing tailored interaction options, all within a framework that encourages social connectivity and recognition of environmental efforts.

## User Settings Page - `settings.html`

Created by Jack Skinner and Giulia Brown, `settings.html` allows CarbonCommuter users to personalize their settings within a user-friendly interface, building on the `base.html` template. The page, titled "Settings," provides a navigation bar suited for both authenticated and guest users, facilitating easy site navigation. It features a form where users can update their first name, last name, username, and email, with a requisite password entry for changes to take effect, emphasizing security. Additionally, a distinct section for account deletion highlights the irreversible nature of this action, warning users of data loss. This setup balances personalization with caution, ensuring users can easily modify their details while being informed of significant actions like account deletion, all encapsulated within a consistent design that includes the site's standard footer.
