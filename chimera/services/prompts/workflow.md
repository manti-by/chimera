1. Retrieve Linear task with highest priority for {project_name} project from TODO column and create an implementation plan for the task using OpenCode.
2. Create a git worktree with a feature branch following the naming convention `opencode/feature/<branch-name>` where `<branch-name>` should be retrieved from `LinearTask.slug`.
3. Add worktree path to the Context model.
4. Create an implementation plan for the task using OpenCode, as an input should be used `LinearTask.text`.
5. Print implementation plan and wait for user input to proceed. If it is necessary return to a previous step with additional comments.
6. Build a feature using implementation plan from the previous step using OpenCode build mode.
7. Check feature using Coderabbit. If there are some suggestions, pass them to the build step and repeat from there.
8. Commit the changes and push the feature branch to the remote repository.
9. Remove the git worktree after the feature is complete and reviewed.
