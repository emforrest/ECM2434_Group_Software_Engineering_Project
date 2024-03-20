
# Directory of Webpages and their Contents

## Home - `./`

The Home page contains information about the application, and is the first page to be visited when users discover the site. It should encourage users to register for an account or login if they already have one, as well as highlight the advantages of using the system, such as linking the Leaderboard. This page should only be accessible to un-authenticated users, any users already logged in should be redirected to the [User Home](#user-home---user) page.

## Login - `./login`

Login follows a standard website login template, with a form that contains fields for the username and password, and a submit button. On submit, the login details should be verified against the database using the built-in Django authentication system. If successfull, the user is redirected to the [User Home](#user-home---user) page, otherwise an error is displayed and they must try again. If this page is visited by an autenticated user, it should instead warn them and give them the option to logout.

## Logout - `./login/logout`

For the Logout page, if the user is authenticated, it should ask for a confirmation if they want to logout, then logout the user if they click the button. If they're not authenticated, it should offer a link to the login/register pages instead.

## Register - `./register`

Register follows a standard website register template, with a form that contains fields for the first and last name, username, email address, password, and another to re-enter the passwor, as well as a prompt to a privacy policy that they must accept. The password is checked against standard security checks (such as length and whether it is a common password), then verified to match the re-entered password. If these checks pass then a new user is created within the database. The user is then redirected to the user home page.

## Privacy Policy `./register/PrivacyPolicy`
CarbonCommuter handles sensitive location data, and the privacy policy outlines how the app uses your personal data. We outline how sensitive location data is deleted after 2 weeks, and that this data is secure and encrypted and stored in a secure database (oracle)

## Leaderboard - `./leaderboard`

The leaderboard page allows anyone without an account to view the status of the leaderbaord. It will display the all time carbon savings for the top 10 users on the system. You can also see the top users this week, and the top groups on the website. 

## Leaderboard `./leaderboard/user_leaderboard`

The user_leaderboard page allows users who are logged in to view additional information on top of the standard leaderboard. You can click on users and groups on the leaderboard to view their public information, You can see how you are doing in comparision to people you are following. 

## User Home - `./user`

The user home page is a dashboard for a user, containing their public and private information including first and last name, email address, username and join date, and their total carbon saving so far, as well as buttons to edit their information, upload a journey or access groups. This page can only be accessed when a user is logged in.

## Upload Journey - `./user/upload` or `./user/upload/<journey-id>`

This is the portal for uploading journeys, and contains a form where the user can select both a location on campus and a location off campus, as well as a mode of transport. This is then submitted, and the distance between the two points should be calculated, along with it's carbon savings. When a journey is successfully uploaded, they are redirected to the `upload/<journey_id>` page, which contains a confirmation, and information about the journey that was just upload. From here, the user can return to the [user home](#user-home---user) page.

## User Settings - `./user/settings`

The user settings page allows a user to make edits to their personal information. It is only available if a user is already logged in. They can edit their first and last name, email address and username. The user must enter their current password in order for the changes to be made to their account.

## Groups Home - `./groups`

The groups home page is the publicly facing page. It displays a list of the top groups, similar to the [Leaderboard](#leaderboard---leaderboard) page and filterable based on different periods of time, e.g. week, month, year. If the user is authenticated, there should also be a list of the user's joined groups, as well as a button to join a group using a code. This page could also display recommnended public groups, depending on the user who's logged in, or generic suggestions if no user is logged in.

## About A Specific Group - `./groups/<group-id>` 

*(Not Completed Yet)*

The group "profile" page displays more in-detail information about a given group, based on the group id specified. Here, users can see the profile picture and description of the group, as well as see a button to join the group if it's public. This page will also display a full list of the members within the groups. If you are a member of the group, you will also be able to visit a tab within the page that displays the leaderboard for just the members within the group, similar to how the [Leaderboard](#leaderboard---leaderboard) page works. Members of the group will also have an option to leave the group from this page.

## Create Group - `./groups/create`

Group creation can be used by any authenticated member. Each group must be given a name, but can also be assigned a profile picture and description. Upon group creation, a unique alpha-numeric code is created, which is stored in the database, and can be shared around to let people join your group.

Groups can also be assigned a visibility, either public or private. A public group can be joined by anyone, and has a button on it's [home page](#about-a-specific-group---groupsgroup-id). A private group can only be joined by users who have the join code, which is only visible to admins on the [home page](#about-a-specific-group---groupsgroup-id). Admins can generate a URL to join the group using this code, which can be shared on social media, for example, or users can enter the code when visiting the [Join Group](#join-group---groupsjoin-or-groupsjoincode) page.

## Join Group - `./groups/join` OR `./groups/join/<code>`

If a code isn't present on the URL, the user will be promoted to enter a join code for a private group. Public groups are only joinable using the button on the [Group Profile](#about-a-specific-group---groupsgroup-id) page, since this redirects the user to this page with the code already attached. The user should be warned about this underneath the box where they enter the code. Upon submission, the code is verified and if it matches a group in the database, they user should be added to the group, and a success page returned. If not, the user should be informed that there doesn't exist a group with that code.

## Leave Group - `./groups/leave`

This page is only accessible via a POST request from the [Groups](#about-a-specific-group---groupsgroup-id) page, and must contain a valid group id to leave that the member is part of. If the group is private, the user will be notified they are about to leave a private group and wont be able to rejoin without the code. If they select yes, all group permissions are revoked and the user is removed from the group.

