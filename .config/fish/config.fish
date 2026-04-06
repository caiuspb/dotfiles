if status is-interactive
    # Commands to run in interactive sessions can go here
end

# zoxide (ersetzt "z")
zoxide init fish | source

# optional: bessere History-Suche mit Pfeiltasten
#bind \e\[A history-search-backward
#bind \e\[B history-search-forward

# alias l auf ls -ahl
function l
    ls -ahl $argv
end

starship init fish | source
