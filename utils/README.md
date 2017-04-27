# Orange and Blue League Utils

Scripts to simplify exporting and importing OOTP16 files in the Orange and Blue League.
Compatible with Linux and Windows (via Cygwin).

## Linux Preparation

First, download the scripts.  
This is most easily accomplished by simply cloning the repository:

```bash
git clone https://github.com/brunner/orangeandblueleague
```

Edit the export script to include your own information:

```bash
gedit orangeandblueleague/utils/exportobl.py
```

Do the same with the import script:

```bash
gedit orangeandblueleague/utils/importobl.py
```

Move the scripts to /usr/local/bin/, per convention:

```bash
sudo mv orangeandblueleague/utils/exportobl.py /usr/local/bin/exportobl && \
sudo mv orangeandblueleague/utils/importobl.py /usr/local/bin/importobl
```

Finally, clean up:

```bash
rm -rf orangeandblueleague
```

## Windows Preparation

First, download and install Cygwin by following the instructions here:
https://cygwin.com/install.html

You need to install the base, python, and wget packages.

Once Cygwin is installed, right click on the desktop icon and click:
Properties > Advanced > Run as Administrator (and check the box)

Then, double click to launch Cygwin.

Finally, you will need to download the importobl.py script.
From the cygwin terminal, run:
```bash
wget https://raw.githubusercontent.com/brunner/orangeandblueleague/master/utils/importobl.py
```

## Import

The import script is a simple shell script that downloads the league file from the league website and unpacks it into the appropriate saved_games directory on your computer. To trigger this, simply run the command from any directory:

Linux:
```bash
importobl
```

Windows:
Note: you will need to run the script from Cygwin. So, double click on Cygwin and type the following command into the prompt:
```bash
python importobl.py
```

The first time you run the command, you will need to manually download some config files into a settings/ directory. Refer to the How-To guide for more information here.

## Recover

Running the importobl command will create a backup of the existing save in the rare case that you want to retrive it. To recover to this backup, you can pass the --recover option to the command- it will move the backup back into the saved_games directory:

Linux:
```bash
importobl --recover
```

Windows:
Note: you will need to run the script from Cygwin. So, double click on Cygwin and type the following command into the prompt:
```bash
python importobl.py --recover
```

## Export

The export script is a Python script that sends an email to the league commissioner containing your most recently exported team file. So, before running the script, you must navigate to your team home page and then select "Export Team to File" from the IMPORT/EXPORT menu in the top right of the window. After, run the command from any directory:

Linux:
```bash
exportobl
```

You will be prompted for the password to your email account. The value is not stored- you must type it every time you execute the script. If your email login is successful, your team file will be mailed to the league commissioner and to yourself, so you have a record of it.

Note: this is untested on Windows, and deprecated on Linux. Linux users can export using the in-game dialog in OOTP 17.