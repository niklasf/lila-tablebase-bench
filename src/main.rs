use std::{
    error::Error,
    fs::File,
    io,
    io::{BufRead, BufReader},
    path::PathBuf,
    time::Instant,
};

use clap::{builder::PathBufValueParser, Parser};
use rayon::prelude::*;

#[derive(Parser)]
struct Opt {
    #[clap(value_parser = PathBufValueParser::new())]
    fens: PathBuf,
    #[clap(long, default_value = "http://localhost:9000/standard")]
    endpoint: String,
}

fn main() -> Result<(), Box<dyn Error>> {
    let opt = Opt::parse();
    let fens: Vec<String> = BufReader::new(File::open(opt.fens)?)
        .lines()
        .collect::<Result<_, io::Error>>()?;

    let client = reqwest::blocking::Client::builder()
        .timeout(None)
        .pool_idle_timeout(None)
        .build()
        .expect("client");

    // With RAYON_NUM_THREADS
    fens.par_iter().for_each(|fen| {
        let before = Instant::now();
        let _ = client
            .get(&opt.endpoint)
            .query(&[("fen", fen)])
            .send()
            .expect("send")
            .text()
            .expect("text");
        println!("{}\t{}", fen, before.elapsed().as_millis());
    });

    Ok(())
}
