# Orange and Blue League

Scripts to simplify exporting and importing OOTP16 files in the Orange and Blue League.

## Preparation (Linux)

First, download the scripts.  
This is most easily accomplished by simply cloning the repository:

```bash
git clone https://github.com/brunner/orangeandblueleague
```

Edit the export script to include your own information:

```bash
gedit orangeandblueleague/utils/exportobl
```

Do the same with the import script:

```bash
gedit orangeandblueleague/utils/importobl
```

Move the scripts to /usr/local/bin/, per convention:

```bash
sudo mv orangeandblueleague/utils/exportobl orangeandblueleague/utils/importobl -t /usr/local/bin
```

Finally, clean up:

```bash
rm -rf orangeandblueleague
```

## Preparation (Windows)

This is experimental, but here is my suggestion:

Copy the experimental importobl script to somewhere on your computer.  
You can find it here: https://github.com/brunner/orangeandblueleague/blob/master/utils/importtest   
Paste the contents of the file into a file called "importobl.py"  
Remove the first line ("#!/usr/bin/env python") from the file.  
Edit the file to replace "orangeandblue.lg" with whatever you have named your league file.  

Make sure you can run python on your computer: https://docs.python.org/2/faq/windows.  
Run the "importobl.py" script.

## Import

The import script is a simple shell script that downloads the league file from the league website and unpacks it into the appropriate saved_games directory on your computer. To trigger this, simply run the command from any directory:

```bash
importobl
```

Running this command will also create a backup of the existing save in the rare case that you want to retrive it. To recover, you can pass the --recover option to the command- it will move the backup back into the saved_games directory:

```bash
importobl --recover
```

## Export

The export script is a Python script that sends an email to the league commissioner containing your most recently exported team file. So, before running the script, you must navigate to your team home page and then select "Export Team to File" from the IMPORT/EXPORT menu in the top right of the window. After, run the command from any directory:

```bash
exportobl
```

You will be prompted for the password to your email account. The value is not stored- you must type it every time you execute the script. If your email login is successful, your team file will be mailed to the league commissioner and to yourself, so you have a record of it.

## Monitor

The monitor script is not intended for personal use- instead, the goal is to deploy the script and use it to monitor the status of the league sim. The monitor script will eventually alert the team when the sim has begun, take screenshots of the results as they happen, and finally send another alert when the league file is ready to be downloaded. This script is a work in progress and is still being tested for bugs.