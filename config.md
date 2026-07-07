**The "Card Rating History" label is hidden by default. To show it, change <i> Show Label </i> to "true"**

### Configuration Options

#### `constantly_show_addon`
- Determines if the rating history should show on both question and answer sides
- Default: "false"
- When "false", only shows on the answer side
- When "true", shows on both question and answer sides

#### `dont_show_reviews_before_manually_forgot`
- Controls whether to hide reviews that occurred before a manual forget
- Default: "false"
- When "true", clears history before manually forgotten cards

#### `hide_manually_forgotten_entries`
- Controls whether manually forgotten entries are hidden from the rating history
- Default: "false"
- Valid values: "true" or "false"

#### `hide_rescheduled_entries`
- Controls whether rescheduled entries are hidden from the rating history
- Default: "false"
- Valid values: "true" or "false"

#### `limit_number`
- Maximum number of review history squares to display
- Default: "30"
- Accepts positive integers

#### `manually_forgot_color`
- Color for manually forgotten cards
- Default: "white"
- Accepts CSS color values (hex, rgb, or color names)

#### `only_show_learning_reviews_in_learning_stage`
- Controls whether to show learning reviews for cards not in the learning stage
- Default: "true"
- When "true", only shows learning reviews for cards currently in learning

#### `overlay_position`
- Controls which corner the rating history uses when `vertical_position` is "overlay"
- Default: "top-right"
- Valid values: "top-left" or "top-right"
- Overlay placement floats over the card instead of taking up layout space

#### `rated_again_color`
- Color for cards rated "Again"
- Default: "#c03c1c"
- Accepts CSS color values

#### `rated_easy_color`
- Color for cards rated "Easy"
- Default: "#006344"
- Accepts CSS color values

#### `rated_good_color`
- Color for cards rated "Good"
- Default: "#B9D870"
- Accepts CSS color values

#### `rated_hard_color`
- Color for cards rated "Hard"
- Default: "#D8A700"
- Accepts CSS color values

#### `show_drop_shadow`
- Controls the drop shadow behind the rating history legend
- Default: "false"
- Valid values: "true" or "false"

#### `show_label`
- Controls visibility of the "Card Rating History" label
- Default: "false"
- Valid values: "true" or "false"

#### `size`
- Controls the CSS zoom level of the rating history display
- Default: "100%"
- Uses percentage values (e.g., "75%", "150%")

#### `vertical_position`
- Determines whether the rating history appears inline or floats over the reviewer
- Default: "bottom"
- Valid values: "top", "bottom", or "overlay"

#### `width`
- Controls the width of the rating history display
- Default: "inherit"
- Accepts CSS width values (e.g., "100px", "50%")

### Notes
- All boolean values should be specified as strings ("true" or "false")
- Color values can be any valid CSS color format
- The add-on will automatically adjust its display based on these settings
- Invalid configurations will fall back to default values
