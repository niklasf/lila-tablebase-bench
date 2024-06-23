use clap::builder::PathBufValueParser;
use clap::Parser;
use rayon::prelude::*;
use std::error::Error;
use std::fs::File;
use std::io;
use std::io::BufRead;
use std::io::BufReader;
use std::path::PathBuf;
use std::time::Instant;

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

    // RAYON_NUM_THREADS

    fens.par_iter().for_each(|fen| {
        let before = Instant::now();
        let _ = reqwest::blocking::Client::new()
            .get(&opt.endpoint)
            .query(&[("fen", fen)])
            .send()
            .expect("send")
            .error_for_status()
            .expect("ok")
            .text()
            .expect("text");
        println!("{}\t{}", fen, before.elapsed().as_millis());
    });

    Ok(())
}
