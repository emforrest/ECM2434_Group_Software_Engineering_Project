CREATE TABLE groups_table (
    GroupID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    TotalSaving DECIMAL(10, 2) DEFAULT 0
);

CREATE TABLE users_table (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    GroupID INT,
    Name VARCHAR(255) NOT NULL,
    JoinDate DATE,
    TotalSaving DECIMAL(10, 2) DEFAULT 0,
    FOREIGN KEY (GroupID) REFERENCES groups_table(GroupID)
);

CREATE TABLE journeys_table (
    JourneyID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Date DATE,
    Time TIME,
    Distance DECIMAL(10, 2),
    TravelMode VARCHAR(50),
    CarbonSaving DECIMAL(10, 2),
    FOREIGN KEY (UserID) REFERENCES users_table(UserID)
);
