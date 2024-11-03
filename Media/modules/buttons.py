from pyrogram.types import *

KL10 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Join", callback_data="deposit")
        ]
    ]
)

def link_buttons(links):
    KL15 = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Link", url=f"{links}"),
            ]
        ]
    )
    return KL15

KL20 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("📜Commands", callback_data="HG1"),
            InlineKeyboardButton("⚙️Settings", callback_data="HG2"),
        ],
        [
            InlineKeyboardButton("💰 Atlantic", callback_data="withdraw")
        ],
        [
            InlineKeyboardButton("❌", callback_data="close")
        ],
    ]
)

KL25 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("✅", callback_data="HG3"),
            InlineKeyboardButton("❌", callback_data="HG4"),
        ],
        [
            InlineKeyboardButton("Copy", callback_data="HG5"),
            InlineKeyboardButton("Forward", callback_data="HG6"),
        ],
        [
            InlineKeyboardButton("🔙Kembali", callback_data="HG0")
        ],
    ]
)

KL30 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🔙Kembali", callback_data="HG2")
        ]
    ]
)

KL35 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🔙Kembali", callback_data="HG0")
        ]
    ]
)

KL40 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Cancel", callback_data="cancel")
        ]
    ]
)

KL45 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("⬇️ Withdraw ⬇️", callback_data="wd")
        ],
        [
            InlineKeyboardButton("Rp.1.000", callback_data="AKI1"),
            InlineKeyboardButton("Rp.10.000", callback_data="AKI2"),
        ],
        [
            InlineKeyboardButton("Rp.20.000", callback_data="AKI3"),
            InlineKeyboardButton("Rp.50.000", callback_data="AKI4"),
        ],
        [
            InlineKeyboardButton("🔙Kembali", callback_data="HG0")
        ],
    ]
)

def withdraw_btn(status):
    KL50 = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅Lanjutkan", callback_data=f"{status}"),
            ],
            [
                InlineKeyboardButton("🔙Kembali", callback_data="withdraw"),
            ],
        ]
    )
    return KL50
