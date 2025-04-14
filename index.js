import jsonfile from "jsonfile";
import moment from "moment";
import simpleGit from "simple-git";
import random from "random";

const path = "date.json";

/**
 * Creates commits with randomized dates in the past year to generate GitHub contribution graph patterns
 * @param {number} totalCommits - Number of commits to generate
 * @returns {Promise} - Promise that resolves when all commits are created and pushed
 */
async function createCommits(totalCommits) {
    const git = simpleGit();
    const commits = [];

    // Create an array of commit operations
    for (let i = 0; i < totalCommits; i++) {
        // Random week (0-54) and day (0-6) in the past year
        const week = random.int(0, 54);
        const day = random.int(0, 6);

        // Calculate date: 1 year back + 1 day + random weeks + random days
        const date = moment()
            .subtract(1, "year")
            .add(1, "day")
            .add(week, "weeks")
            .add(day, "days")
            .format();

        commits.push({ date });
    }

    // Process commits sequentially
    for (const [index, { date }] of commits.entries()) {
        console.log(`Creating commit ${index + 1}/${totalCommits}: ${date}`);

        // Write date to file
        await jsonfile.writeFile(path, { date });

        // Add, commit with the specified date
        await git.add([path]);
        await git.commit(date, { "--date": date });
    }

    // Push all commits at once
    console.log("Pushing all commits to remote repository...");
    await git.push();
    console.log("Done! All commits have been created and pushed.");
}

// Single function to mark a specific coordinate on the contribution graph
async function markSpecificSpot(x, y) {
    const git = simpleGit();

    const date = moment()
        .subtract(1, "year")
        .add(1, "day")
        .add(x, "weeks")
        .add(y, "days")
        .format();

    console.log(`Marking specific spot at week ${x}, day ${y}: ${date}`);

    await jsonfile.writeFile(path, { date });
    await git.add([path]);
    await git.commit(date, { "--date": date });
    await git.push();

    console.log("Specific spot marked successfully!");
}

// Start the commit creation process
createCommits(100).catch((error) => {
    console.error("Error creating commits:", error);
});
