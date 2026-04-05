import click
from financesync.commands import open, sync, refresh

@click.command()
@click.option("--sync", "sync_flag", is_flag=True, help="Sync transactions from Gmail to Google Sheets")
@click.option("--open", "open_flag", is_flag=True, help="Open the Google Sheet in the browser")
@click.option("--force-refresh", "force_refresh_flag", is_flag=True, help="Refresh Google API credentials")
def run(sync_flag, open_flag, force_refresh_flag):
    if not sync_flag and not open_flag and not force_refresh_flag:
        print("No command provided. Use --help for more information.")

    if force_refresh_flag:
        refresh()
    if sync_flag:
        sync()
    if open_flag:
        open()

if __name__ == "__main__":
    run()