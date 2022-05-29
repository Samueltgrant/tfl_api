from website import create_app

app = create_app()
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres: // byhxcaqmpaygky: 965f695180e2ef9bc0661fca243c36006c6de90b2390c7a5cccdddeaf9a505e8@ec2-34-230-153-41.compute-1.amazonaws.com:5432/d4quaupiqp3lpf'
if __name__ == '__main__':
    app.run(debug=True)
