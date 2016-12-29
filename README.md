# Orange and Blue League

Scripts to simplify exporting and importing OOTP16 files in the Orange and Blue League.

## Preparation

First, download the scripts.  
This is most easily accomplished by simply cloning the repository:

```bash
git clone https://github.com/brunner/orangeandblueleague
```

However, you can accomplish the same by manually downloading and unpacking the archive:

```bash
mkdir orangeandblueleague \
  && wget https://github.com/brunner/orangeandblueleague/archive/master.zip \
  && unzip master.zip -d orangeandblueleague \
  && rm master.zip
```

Edit the export script to include your own information:

```bash
gedit orangeandblueleague/exportobl
```

Do the same with the import script:

```bash
gedit orangeandblueleague/importobl
```

Next, make the scripts executable:

```bash
chmod +x orangeandblueleague/exportobl orangeandblueleague/importobl
```

Move the scripts to /usr/local/bin/, per convention:

```bash
sudo mv orangeandblueleague/exportobl orangeandblueleague/importobl -t /usr/local/bin
```

Finally, clean up:

```bash
rm -rf orangeandblueleague
```

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