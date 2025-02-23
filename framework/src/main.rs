use crate::session::Session;
use args::{Args, Commands};
use clap::Parser;
use common::Solution;
use miette::Result;
mod args;
#[macro_use]
mod misc;
mod commands;
mod formatter;
mod session;

fn main() -> Result<()> {
    let args = Args::parse();

    let session = match &args.token {
        Some(token) => Ok(Session::new(token)),
        None => Session::from_file(),
    };

    match &args.subcommand {
        Commands::Verify => commands::verify::verify(&session?, &args.address)?,
        Commands::Timer(e) => commands::timer::timer(e)?,
        Commands::Init(e) => commands::init::init(&session?, e, &args)?,
        Commands::Run(cmd) => commands::run::run(cmd)?,
        // Commands::RunAll(cmd) => commands::run_all::run(cmd)?,
        Commands::List(cmd) => commands::list::list(cmd)?,
        Commands::Submit(e) => commands::submit::submit(&session?, e, &args)?,
    }

    Ok(())
}

fn get_year(year: u16) -> &'static [Solution] {
    match year {
        // 2020 => aoc_2020::SOLUTIONS,
        // 2021 => aoc_2021::SOLUTIONS,
        // 2022 => aoc_2022::SOLUTIONS,
        // 2023 => aoc_2023::SOLUTIONS,
        2024 => aoc_2024::SOLUTIONS,
        _ => &[],
    }
}
