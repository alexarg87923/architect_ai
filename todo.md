1. Dive deeper into the interaction between the Agent and the User. 
    - Improve the interaction/ questions asked.
    - Improve the instructions for roadmap generation (currently the generated nodes seem to be too high level).
    - Ex: Current Node --> Frontend Development, Should be instead --> setup frontend boilerplate, build dashboard/main page, perhaps design some stuff, build out sidebar, build out chatbot, etc.
    - Node completion times should be much shorter, check if it is the LLM script instructions that is causing this.
    - Perhaps the AI doesn't know that this is for personal projects that will usually last between 1 week to 2-3 months.

3. Add rate limiting to the backend.

6. Implement progress tracking functionality
    - Add ability to mark roadmap nodes as completed
    - Update node visual states (completed, in-progress, blocked) --> Add notes to a specific Node (expanded Node)
    - Add progress percentage to project overview
    - Auto-scroll to current active node in roadmap *****

7. Add roadmap editing capabilities
    - Allow users to modify node descriptions and timelines
    - Add/remove nodes from existing roadmaps
    - Reorder nodes or create dependencies between them
    - Save and version roadmap changes

8. Improve visualization and UX
    - Add zoom/pan controls for large roadmaps
    - Implement mini-map for navigation
    - Add node search/filter functionality --> ADD CMD+K search bar that appears on the top to search through available nodes/ projects
    - Improve mobile responsiveness for Canvas component

9. Add data persistence and sync
    - Real-time updates when roadmap changes
    - Backup/export roadmap data (JSON, PDF)
    - Import existing project plans
    - Collaboration features for team projects

10. Error handling and user feedback
    - Better error messages for API failures
    - Loading states during roadmap generation
    - Retry mechanisms for failed requests
    - User confirmation dialogs for destructive actions

11. Protect the Admin Panel
    - Used to create new account to give to people
    - Create superuser boolean in the User model
    - Create script to create admin account (mine) --> gitignore that script
    - Protect the admin route to only allow superusers to access it