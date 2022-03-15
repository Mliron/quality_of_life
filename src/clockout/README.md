# Clockout
Script that allows you to manually time various events.

## Details
Timing is done by saving timestamps at the start and at the end.<br/>
Timestamp format: `dd-mm-yyyy hh:mm:ss`<br/>
Save file format: JSON<br/>
```
clockout_data.json:
{
    "tag": [
        {
            "start": timestamp,
            "finish": [timestamp | null]
        },
        ...
    ],
    ...
}
```

## Examples
`python3 clockout.py --toggle` - Starts or finishes a session under a tag `None`<br/>
`python3 clockout.py --toggle -t example` - Starts or finishes a session under a tag `example`<br/>
`python3 clockout.py --list 3` - Lists 3 or maximum available sessions from all tags<br/>
`python3 clockout.py --tag example --find 2022` - Lists all sessions that started in 2022 under a tag `example`<br/>

## System compatibility
Should work everywhere with python3.6 and later

## Plans for the future
No plans, but may add something if something comes to mind
