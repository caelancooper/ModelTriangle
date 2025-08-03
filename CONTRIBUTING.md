## Adding New Features

### Adding New Agents:
Add to `self.agents` list in `__init__()`:
```python
{"name": "Your Model", "model": "provider/model-name"}
```
### Adding New UI Elements:
Extend setup_gui() method - all UI uses CustomTkinter
Key Methods to Know:

append_text(): Thread-safe text display
save_chat(): Conversation persistence
get_chat_completion(): Agent iteration logic

### Adding Code Generation & Execution
Displayable
In-text executions and results before thought is finished

### Database Integration
Integration of APIs for enterprise use is ***Priority #1***

### Thank You
Thank you all for reading this project file
All engagement with this app is welcome