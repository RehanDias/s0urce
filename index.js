import jsonfile from "jsonfile";
import moment from "moment";
import simpleGit from "simple-git";
import random from "random";

const path = "date.json";

/**
 * Creates commits with naturally random patterns to simulate human behavior
 * @param {number} totalCommits - Number of commits to generate
 * @returns {Promise} - Promise that resolves when all commits are created and pushed
 */
async function createCommits(totalCommits) {
    // Tambahkan buffer 5 menit untuk menghindari masalah timing
    const safetyBuffer = 5; // menit
    const today = moment().subtract(safetyBuffer, "minutes");
    const fullYear = moment().subtract(365, "days");

    console.log(`Running on ${moment().format("YYYY-MM-DD HH:mm:ss")}`);
    console.log(
        `Using safety cutoff time: ${today.format(
            "YYYY-MM-DD HH:mm:ss"
        )} (with ${safetyBuffer} minute buffer)`
    );
    console.log(`Ensuring no commits will be created past this time`);

    // Helper function untuk memastikan tanggal tidak di masa depan
    function ensureNotFuture(dateToCheck) {
        return moment(dateToCheck).isAfter(today) ? false : true;
    }

    const git = simpleGit();
    const commits = [];

    // Calendar to track commits per day
    const calendar = {};

    // Initialize calendar with all dates in the past year
    let current = moment(fullYear);
    while (current.isSameOrBefore(today)) {
        const dateKey = current.format("YYYY-MM-DD");
        calendar[dateKey] = 0;
        current.add(1, "day");
    }

    // Simulate human patterns
    // 1. Work sprints (periods of high activity)
    // 2. Vacations/breaks (periods of no activity)
    // 3. Regular work patterns (weekdays vs weekends)
    // 4. Varied daily intensity
    // 5. Random "emergency commits" late at night

    // Generate 2-4 work sprint periods randomly throughout the year
    const numSprints = random.int(2, 4);
    const sprintPeriods = [];

    for (let i = 0; i < numSprints; i++) {
        const sprintStart = random.int(0, 320); // Days from the start (leaving buffer at end of year)
        const sprintLength = random.int(5, 14); // 5-14 day sprint

        sprintPeriods.push({
            start: moment(fullYear).add(sprintStart, "days"),
            end: moment(fullYear).add(sprintStart + sprintLength, "days"),
        });
    }

    // Generate 2-3 vacation periods (no commits)
    const numVacations = random.int(2, 3);
    const vacationPeriods = [];

    for (let i = 0; i < numVacations; i++) {
        const vacationStart = random.int(0, 330); // Days from the start
        const vacationLength = random.int(3, 14); // 3-14 day vacation

        vacationPeriods.push({
            start: moment(fullYear).add(vacationStart, "days"),
            end: moment(fullYear).add(vacationStart + vacationLength, "days"),
        });
    }

    // Create preferred working days pattern (some people work weekends, some don't)
    const workStyle = random.int(1, 5);
    const preferredDays = [];

    if (workStyle === 1) {
        // Weekend warrior - more commits on weekends
        preferredDays.push(0, 6); // Sunday, Saturday
    } else if (workStyle === 2) {
        // Standard worker - more commits on weekdays
        preferredDays.push(1, 2, 3, 4, 5); // Monday-Friday
    } else if (workStyle === 3) {
        // Mid-week specialist
        preferredDays.push(2, 3, 4); // Tuesday-Thursday
    } else if (workStyle === 4) {
        // Erratic - random preferred days
        const numDays = random.int(2, 5);
        const allDays = [0, 1, 2, 3, 4, 5, 6];
        for (let i = 0; i < numDays; i++) {
            const index = random.int(0, allDays.length - 1);
            preferredDays.push(allDays[index]);
            allDays.splice(index, 1);
        }
    } else {
        // Works almost every day
        preferredDays.push(0, 1, 2, 3, 4, 5, 6);
    }

    // Create a randomized project intensity curve
    // Higher intensity in recent months but with natural variations
    current = moment(fullYear);
    while (current.isSameOrBefore(today)) {
        const dateKey = current.format("YYYY-MM-DD");
        const daysFromStart = current.diff(fullYear, "days");
        const dayOfWeek = current.day();
        let baseIntensity = 0;

        // Check if date is in a vacation period
        const inVacation = vacationPeriods.some(
            (period) =>
                current.isSameOrAfter(period.start) &&
                current.isSameOrBefore(period.end)
        );

        if (inVacation) {
            // Possibility of a very occasional commit during vacation
            baseIntensity = random.float() < 0.05 ? 1 : 0;
        } else {
            // Check if date is in a sprint period
            const inSprint = sprintPeriods.some(
                (period) =>
                    current.isSameOrAfter(period.start) &&
                    current.isSameOrBefore(period.end)
            );

            // Natural project progression - more activity as year progresses
            // But with realistic fluctuations
            const projectProgression = Math.min(
                1,
                daysFromStart / 365 + random.float() * 0.3
            );

            // Base intensity calculation
            if (inSprint) {
                baseIntensity = random.int(3, 8); // High activity during sprints
            } else if (preferredDays.includes(dayOfWeek)) {
                baseIntensity = Math.floor(
                    projectProgression * random.int(0, 4)
                ); // Preferred working days
            } else {
                baseIntensity = Math.floor(
                    projectProgression * random.int(0, 2)
                ); // Non-preferred days
            }

            // Add randomness to create more natural patterns
            const randomFactor = random.float() < 0.15 ? random.int(1, 3) : 0;

            // Some days might have unusual activity
            const unusualDay = random.float() < 0.03; // 3% chance of an unusual day
            if (unusualDay) {
                if (random.float() < 0.5) {
                    // Unusually high activity
                    baseIntensity = random.int(5, 12);
                } else {
                    // Unusually low activity on expected work day
                    baseIntensity = 0;
                }
            }

            // Final intensity with adjustments
            baseIntensity += randomFactor;
        }

        calendar[dateKey] = baseIntensity;
        current.add(1, "day");
    }

    // Convert calendar to a list of commits
    Object.entries(calendar).forEach(([dateStr, commitCount]) => {
        for (let i = 0; i < commitCount; i++) {
            // More realistic time patterns
            let randomHour, randomMinute, randomSecond;

            // Format the date
            const dateObj = moment(dateStr);

            // PERBAIKAN: Skip future dates secara explicit
            if (dateObj.isAfter(today)) {
                console.log(`Skipping future date: ${dateStr}`);
                continue;
            }

            // If it's today, make sure we don't create future times
            if (dateObj.isSame(today, "day")) {
                const currentHour = today.hour();
                randomHour = random.int(0, Math.max(0, currentHour - 1)); // At least 1 hour before now

                if (randomHour === currentHour - 1) {
                    const currentMinute = today.minute();
                    randomMinute = random.int(
                        0,
                        Math.max(0, currentMinute - 10)
                    ); // Lebih aman: 10 menit sebelum

                    if (randomMinute === currentMinute - 10) {
                        const currentSecond = today.second();
                        randomSecond = random.int(
                            0,
                            Math.max(0, currentSecond - 20)
                        ); // Lebih aman: 20 detik sebelum
                    } else {
                        randomSecond = random.int(0, 59);
                    }
                } else {
                    randomMinute = random.int(0, 59);
                    randomSecond = random.int(0, 59);
                }
            } else {
                // For past dates, use normal time distribution
                // 10% chance of odd-hours commit (late night or early morning)
                if (random.float() < 0.1) {
                    randomHour = random.int(0, 23);
                } else {
                    // Most commits during working hours with lunch break dip
                    if (random.float() < 0.7) {
                        // Morning or afternoon work hours
                        randomHour =
                            random.float() < 0.5
                                ? random.int(9, 12)
                                : random.int(13, 18);
                    } else {
                        // Evening coding sessions
                        randomHour = random.int(19, 23);
                    }
                }

                // People tend to commit on rounded times or with certain patterns
                if (random.float() < 0.3) {
                    // Rounded time
                    const roundedMinutes = [0, 15, 30, 45];
                    const roundedSeconds = [0, 30];
                    randomMinute =
                        roundedMinutes[
                            random.int(0, roundedMinutes.length - 1)
                        ];
                    randomSecond =
                        roundedSeconds[
                            random.int(0, roundedSeconds.length - 1)
                        ];
                } else {
                    // Random time
                    randomMinute = random.int(0, 59);
                    randomSecond = random.int(0, 59);
                }
            }

            const date = moment(dateStr)
                .hour(randomHour)
                .minute(randomMinute)
                .second(randomSecond)
                .format();

            // PERBAIKAN: Final check untuk memastikan tidak ada commit masa depan
            if (!ensureNotFuture(date)) {
                console.log(`Skipping future commit time: ${date}`);
                continue;
            }

            commits.push({ date });
        }
    });

    // Add a few totally random commits throughout the year for extra randomness
    const randomCommitCount = random.int(5, 15);
    for (let i = 0; i < randomCommitCount; i++) {
        const daysInYear = today.diff(fullYear, "days");
        const randomDaysFromStart = random.int(0, daysInYear - 1); // PERBAIKAN: -1 untuk extra safety

        const randomDate = moment(fullYear).add(randomDaysFromStart, "days");

        // PERBAIKAN: Double check untuk memastikan tanggal tidak di masa depan
        if (!ensureNotFuture(randomDate)) {
            console.log(`Skipping random future date: ${randomDate.format()}`);
            continue;
        }

        // Set time based on whether it's today or past
        let randomHour, randomMinute, randomSecond;

        if (randomDate.isSame(today, "day")) {
            // For today, use time that's in the past
            const currentHour = today.hour();
            randomHour = random.int(0, Math.max(0, currentHour - 2)); // PERBAIKAN: -2 jam untuk lebih aman
            if (randomHour === currentHour - 2) {
                randomMinute = random.int(0, Math.max(0, today.minute() - 15)); // PERBAIKAN: -15 menit untuk lebih aman
                randomSecond = random.int(0, 59);
            } else {
                randomMinute = random.int(0, 59);
                randomSecond = random.int(0, 59);
            }
        } else {
            // For past days, use any time
            randomHour = random.int(0, 23);
            randomMinute = random.int(0, 59);
            randomSecond = random.int(0, 59);
        }

        const date = randomDate
            .hour(randomHour)
            .minute(randomMinute)
            .second(randomSecond)
            .format();

        // PERBAIKAN: Final check untuk memastikan tidak ada commit masa depan
        if (!ensureNotFuture(date)) {
            console.log(`Skipping future random commit time: ${date}`);
            continue;
        }

        commits.push({ date });
    }

    // Sort commits chronologically
    commits.sort((a, b) => moment(a.date).valueOf() - moment(b.date).valueOf());

    console.log(`Total commits generated: ${commits.length}`);

    // Process commits sequentially
    for (const [index, { date }] of commits.entries()) {
        // PERBAIKAN: Final safety check sebelum membuat commit
        if (!ensureNotFuture(date)) {
            console.log(`Final check - Skipping future commit: ${date}`);
            continue;
        }

        console.log(`Creating commit ${index + 1}/${commits.length}: ${date}`);

        // Write date to file
        await jsonfile.writeFile(path, { date });

        // Add, commit with the specified date
        await git.add([path]);
        await git.commit(`Update at ${date}`, { "--date": date });
    }

    // Push all commits at once
    console.log("Pushing all commits to remote repository...");
    await git.push();
    console.log(
        `Done! Created ${commits.length} commits with natural human-like patterns.`
    );
}

// Start the commit creation process
createCommits(random.int(500, 800)).catch((error) => {
    console.error("Error creating commits:", error);
});
